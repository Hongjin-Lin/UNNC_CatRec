"""Build cat_profiles.pkl (embedding vector DB) from campus_cats_library images.

Model: AvitoTech/DINO-v2-small-for-animal-identification (DINOv2-small fine-tuned)
Prioritizes local model_save/ directory, falls back to HuggingFace download.

Usage:
    cd backend
    python build_embeddings.py

Outputs:
    data/cat_profiles.pkl
"""
from __future__ import annotations

import pickle
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).parent.parent
LIBRARY_DIR = ROOT / "campus_cats_library"
OUT_PATH = Path(__file__).parent / "data" / "cat_profiles.pkl"
BASE_CKP = "facebook/dinov2-small"
AVITO_REPO = "AvitoTech/DINO-v2-small-for-animal-identification"
AVITO_FILE = "model.safetensors"
LOCAL_MODEL_DIR = ROOT / "model_save"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def load_model():
    import torch
    import torch.nn as nn
    import safetensors.torch
    from transformers import AutoModel, AutoImageProcessor
    from huggingface_hub import hf_hub_download

    class Model(nn.Module):
        def __init__(self):
            super().__init__()
            self.backbone = AutoModel.from_pretrained(BASE_CKP)
            self.processor = AutoImageProcessor.from_pretrained(BASE_CKP, use_fast=True)

        def forward(self, images):
            dev = next(self.parameters()).device
            inputs = self.processor(images=images, return_tensors="pt").to(dev)
            out = self.backbone(**inputs)
            feats = out.last_hidden_state[:, 0, :]
            return feats

    print(f"Loading base model: {BASE_CKP}")
    model = Model()

    local_avito = LOCAL_MODEL_DIR / AVITO_FILE
    if local_avito.exists():
        print(f"Loading AvitoTech weights from local: {local_avito}")
        weights_path = str(local_avito)
    else:
        print(f"Downloading AvitoTech weights from {AVITO_REPO} ...")
        weights_path = hf_hub_download(repo_id=AVITO_REPO, filename=AVITO_FILE)

    state_dict = safetensors.torch.load_file(weights_path)
    model.load_state_dict(state_dict, strict=False)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device).eval()
    print(f"Model loaded on {device}")
    return model, device


def embed_images(image_paths: list[Path], model, device) -> np.ndarray | None:
    """Return mean L2-normalised embedding for a list of image paths."""
    import torch
    import torch.nn.functional as F

    vecs = []
    for p in image_paths:
        try:
            image = Image.open(p).convert("RGB")
        except Exception as e:
            print(f"  [skip] {p.name}: {e}")
            continue
        with torch.no_grad():
            feat = model([image])
            feat = F.normalize(feat, dim=1)
        vecs.append(feat[0].cpu().numpy())

    if not vecs:
        return None
    mean_vec = np.mean(vecs, axis=0)
    mean_vec = mean_vec / (np.linalg.norm(mean_vec) + 1e-8)
    return mean_vec.astype(np.float32)


def main():
    cat_dirs = sorted(p for p in LIBRARY_DIR.iterdir() if p.is_dir())
    print(f"Found {len(cat_dirs)} cat folders in {LIBRARY_DIR}")

    model, device = load_model()

    profiles = []
    embeddings = []
    skipped = []

    for cat_dir in cat_dirs:
        name = cat_dir.name
        image_paths = sorted(p for p in cat_dir.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS)
        if not image_paths:
            print(f"[skip] No images in '{name}/'")
            skipped.append(name)
            continue

        print(f"Processing '{name}' ({len(image_paths)} images) ...")
        vec = embed_images(image_paths, model, device)
        if vec is None:
            print(f"  [skip] All images failed for '{name}'")
            skipped.append(name)
            continue

        profiles.append({"name": name})
        embeddings.append(vec)

    if not profiles:
        print("No profiles built. Exiting.")
        sys.exit(1)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "wb") as f:
        pickle.dump({"profiles": profiles, "embeddings": embeddings}, f)

    print(f"\nDone. {len(profiles)} profiles saved to {OUT_PATH}")
    if skipped:
        print(f"Skipped ({len(skipped)}): {skipped}")


if __name__ == "__main__":
    main()
