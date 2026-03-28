import os
# 必须在 import huggingface_hub 之前设置
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

from huggingface_hub import snapshot_download

try:
    print("开始下载/校验模型...")
    snapshot_download(
        repo_id="google/siglip2-giant-opt-patch16-384",
        local_dir="./model_save", # 建议直接下载到当前项目的文件夹，看得见摸得着
        max_workers=8,            # 开启多线程
        token=False               # 忽略 token 警告
    )
    print("恭喜！模型已准备就绪。")
except Exception as e:
    print(f"出错啦: {e}")