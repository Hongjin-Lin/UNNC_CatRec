from __future__ import annotations
import torch
import torch.nn.functional as F
from PIL import Image
from transformers import SiglipModel, SiglipProcessor
from safetensors.torch import load_file
from huggingface_hub import hf_hub_download
from pathlib import Path

DEFAULT_REGISTRY_PATH = Path("cat_registry.pt")


class CatRecognizer:
    def __init__(self, registry_path: str | Path = DEFAULT_REGISTRY_PATH):
        self.registry_path = Path(registry_path)

        ckpt = "google/siglip2-giant-opt-patch16-384"
        self.processor = SiglipProcessor.from_pretrained(ckpt)
        self.clip = SiglipModel.from_pretrained(ckpt)

        weights_path = hf_hub_download(repo_id="AvitoTech/SigLIP2-giant", filename="model.safetensors")
        state_dict = load_file(weights_path)
        self.clip.load_state_dict(state_dict, strict=False)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.clip = self.clip.to(self.device).eval()

        # 已注册的猫咪档案: {name: prototype_embedding}
        self.registry: dict[str, torch.Tensor] = {}
        self._load_registry()

    # ── 持久化 ────────────────────────────────────────────────────────────────

    def _load_registry(self):
        """从磁盘加载已有的注册档案（若存在）"""
        if self.registry_path.exists():
            data = torch.load(self.registry_path, map_location=self.device)
            self.registry = data
            print(f"[load] 已从 {self.registry_path} 加载 {len(self.registry)} 只猫咪档案："
                  f" {list(self.registry.keys())}")
        else:
            print(f"[load] 未找到档案文件，从空档案开始")

    def save_registry(self):
        """将当前注册档案保存到磁盘"""
        torch.save(self.registry, self.registry_path)
        print(f"[save] 档案已保存到 {self.registry_path}")

    def list_cats(self) -> list[str]:
        """列出所有已注册的猫咪名字"""
        return list(self.registry.keys())

    def remove(self, name: str):
        """删除某只猫咪的档案（需手动调用 save_registry 持久化）"""
        if name not in self.registry:
            raise KeyError(f"未找到猫咪 '{name}'")
        del self.registry[name]
        print(f"[remove] '{name}' 已从档案中删除")

    # ── 核心功能 ──────────────────────────────────────────────────────────────

    @torch.no_grad()
    def _embed(self, images: list) -> torch.Tensor:
        """提取并 L2 归一化的图片嵌入，返回 shape (N, D)"""
        inputs = self.processor(images=images, return_tensors="pt").to(self.device)
        feats = self.clip.get_image_features(**inputs)  # (N, D)
        return F.normalize(feats, dim=1)

    def register(self, name: str, image_paths: list[str], save: bool = True) -> torch.Tensor:
        """
        注册一只猫咪。
        name        : 猫咪名字（标识符）
        image_paths : 该猫咪的多张照片路径
        save        : 注册后自动保存到磁盘（默认 True）
        返回原型向量（已归一化）
        """
        images = [Image.open(p).convert("RGB") for p in image_paths]
        embeddings = self._embed(images)          # (N, D)
        prototype = F.normalize(embeddings.mean(dim=0, keepdim=True), dim=1)  # (1, D)
        self.registry[name] = prototype
        print(f"[register] '{name}' 已注册，使用 {len(images)} 张照片")
        if save:
            self.save_registry()
        return prototype

    def identify(self, image_paths: str | list[str], top_k: int = 3) -> list[dict] | list[list[dict]]:
        """
        识别一张或多张图片属于哪只已注册猫咪。
        image_paths : 单个路径字符串，或路径字符串列表
        top_k       : 每张图片返回概率最高的前 k 个结果
        返回值:
            单张图片 -> list[dict]            每项含 name / similarity / probability
            多张图片 -> list[list[dict]]      外层按输入顺序，内层同上
        """
        if not self.registry:
            raise RuntimeError("还没有注册任何猫咪，请先调用 register()")

        single = isinstance(image_paths, str)
        paths = [image_paths] if single else image_paths

        images = [Image.open(p).convert("RGB") for p in paths]
        queries = self._embed(images)  # (N, D)

        names = list(self.registry.keys())
        prototypes = torch.cat([self.registry[n] for n in names], dim=0)  # (K, D)

        # 批量余弦相似度：(N, D) x (D, K) -> (N, K)
        sims = queries @ prototypes.T
        # 温度缩放 softmax -> (N, K)
        probs = torch.softmax(sims / 0.07, dim=1)

        all_results = []
        for img_sims, img_probs in zip(sims, probs):
            row = sorted(
                [{"name": n, "similarity": img_sims[i].item(), "probability": img_probs[i].item()}
                 for i, n in enumerate(names)],
                key=lambda x: x["probability"],
                reverse=True,
            )
            all_results.append(row[:top_k])

        return all_results[0] if single else all_results

    def is_same_cat(
        self,
        name: str,
        image_paths: str | list[str],
        threshold: float = 0.5,
    ) -> dict | list[dict]:
        """
        判断一张或多张图片是否是指定的猫咪。
        threshold : probability 阈值，超过则认为是同一只
        单张图片返回 dict，多张图片返回 list[dict]。
        每项含 {is_match, probability, similarity, image_path}
        """
        single = isinstance(image_paths, str)
        paths = [image_paths] if single else image_paths

        batch_results = self.identify(paths)  # list[list[dict]]

        output = []
        for path, results in zip(paths, batch_results):
            match = next((r for r in results if r["name"] == name), None)
            if match is None:
                output.append({"image_path": path, "is_match": False, "probability": 0.0, "similarity": -1.0})
            else:
                output.append({
                    "image_path": path,
                    "is_match": match["probability"] >= threshold,
                    "probability": match["probability"],
                    "similarity": match["similarity"],
                })

        return output[0] if single else output


# ── 使用示例 ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    rec = CatRecognizer()  # 启动时自动加载已有档案

    # 只有首次运行（或档案不存在）时才需要注册
    if "卷卷" not in rec.list_cats():
        rec.register("卷卷", [
            "images/卷卷/train_1.jpg",
            "images/卷卷/train_2.jpg",
            "images/卷卷/train_3.jpg",
            "images/卷卷/train_4.jpg",
            "images/卷卷/train_5.jpg",
            "images/卷卷/train_6.jpg",
            "images/卷卷/train_7.jpg",
            "images/卷卷/train_8.jpg",
            "images/卷卷/train_9.jpg",
            "images/卷卷/train_10.jpg",
        ])

    if "橙子" not in rec.list_cats():
        rec.register("橙子", [
            "images/橙子/train_1.jpg",
            "images/橙子/train_2.jpg",
            "images/橙子/train_3.jpg",
            "images/橙子/train_4.jpg",
            "images/橙子/train_5.jpg",
            "images/橙子/train_6.jpg",
            "images/橙子/train_7.jpg",
            "images/橙子/train_8.jpg",
            "images/橙子/train_9.jpg",
            "images/橙子/train_10.jpg",
        ])

    if "粑粑柑" not in rec.list_cats():
        rec.register("粑粑柑", [
            "images/粑粑柑/train_1.jpg",
            "images/粑粑柑/train_2.jpg",
            "images/粑粑柑/train_3.jpg",
        ])

    if "黄苹果" not in rec.list_cats():
        rec.register("黄苹果", [
            "images/黄苹果/train_1.jpg",
            "images/黄苹果/train_2.jpg",
            "images/黄苹果/train_3.jpg",
            "images/黄苹果/train_4.jpg",
            "images/黄苹果/train_5.jpg",
        ])

    print(f"\n当前档案中的猫咪：{rec.list_cats()}")

    # 识别多张图片
    test_images = [
        "images/卷卷/train_11.jpg",
        "images/卷卷/train_12.jpg",
        "images/卷卷/train_13.jpg",
        "images/卷卷/train_14.jpg",
        "images/卷卷/train_15.jpg",
        "images/卷卷/train_16.jpg",
        "images/卷卷/train_17.jpg",
        "images/卷卷/train_18.jpg",
        "images/橙子/train_11.jpg",
        "images/橙子/train_13.jpg",
        "images/橙子/train_14.jpg",
        "images/橙子/train_12.jpg",
        "images/粑粑柑/train_4.jpg",
        "images/粑粑柑/train_5.jpg",
        "images/黄苹果/train_6.jpg",
        "images/黄苹果/train_7.jpg",
        "images/黄苹果/train_8.jpg",
        "images/黄苹果/train_9.jpg",
        "images/黄苹果/train_10.jpg",
    ]
    results = rec.identify(test_images, top_k=3)
    print("\n识别结果：")
    for path, top in zip(test_images, results):
        print(f"  [{path}]")
        for r in top:
            print(f"    {r['name']:12s}  相似度={r['similarity']:.4f}  概率={r['probability']:.1%}")
