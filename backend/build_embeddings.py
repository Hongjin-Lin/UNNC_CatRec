"""Build cat_profiles.pkl from cats.json + campus_cats_library images.

Usage:
    cd backend
    python build_profiles.py

Outputs:
    data/cat_profiles.pkl
"""
from __future__ import annotations

import io
import json
import pickle
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).parent.parent
CATS_JSON = ROOT / "cats.json"
LIBRARY_DIR = ROOT / "campus_cats_library"
OUT_PATH = Path(__file__).parent / "data" / "cat_profiles.pkl"
MODEL_NAME = "openai/clip-vit-large-patch14"  # Using available CLIP model


def load_model():
    from transformers import AutoProcessor, AutoModel
    import torch

    print(f"Loading model {MODEL_NAME} ...")
    processor = AutoProcessor.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME)
    model.eval()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    model = model.to(device)
    print(f"Model loaded on {device}")
    return processor, model, device


def embed_images(image_paths: list[Path], processor, model, device) -> np.ndarray:
    """Return mean L2-normalised embedding for a list of image paths."""
    import torch

    vecs = []
    for p in image_paths:
        try:
            image = Image.open(p).convert("RGB")
        except Exception as e:
            print(f"  [skip] {p.name}: {e}")
            continue
        inputs = processor(images=image, return_tensors="pt").to(device)
        with torch.no_grad():
            features = model.get_image_features(**inputs)
        vec = features[0].cpu().numpy()
        vec = vec / (np.linalg.norm(vec) + 1e-8)
        vecs.append(vec)

    if not vecs:
        return None

    mean_vec = np.mean(vecs, axis=0)
    mean_vec = mean_vec / (np.linalg.norm(mean_vec) + 1e-8)
    return mean_vec.astype(np.float32)


def main():
    with open(CATS_JSON, encoding="utf-8") as f:
        cats = json.load(f)["list"]

    print(f"Found {len(cats)} cats in cats.json")

    processor, model, device = load_model()

    profiles = []
    embeddings = []
    skipped = []

    for cat in cats:
        name = cat.get("Name", "").strip()
        if not name:
            continue

        cat_dir = LIBRARY_DIR / name
        if not cat_dir.exists():
            print(f"[skip] No folder for '{name}'")
            skipped.append(name)
            continue

        image_paths = sorted(
            p for p in cat_dir.iterdir()
            if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")
        )
        if not image_paths:
            print(f"[skip] No images in '{name}/'")
            skipped.append(name)
            continue

        print(f"Processing '{name}' ({len(image_paths)} images) ...")
        vec = embed_images(image_paths, processor, model, device)
        if vec is None:
            print(f"  [skip] All images failed for '{name}'")
            skipped.append(name)
            continue

        personality = []
        if cat.get("Is_friendly") == "是":
            personality.append("亲人")
        elif cat.get("Is_friendly") == "否":
            personality.append("怕生")

        profile = {
            "name": name,
            "location": cat.get("Discovery_location") or "",
            "personality": personality,
            "tnr_status": bool(cat.get("Is_neutered", False)),
            "notes": cat.get("Description") or "",
        }

        profiles.append(profile)
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
