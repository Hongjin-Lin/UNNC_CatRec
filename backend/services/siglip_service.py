"""SigLIP2-Giant inference service.

Model: google/siglip2-giant-patch16-384
Loaded lazily on first call and cached in module globals.
"""
from __future__ import annotations

import io
import pickle
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

_model = None
_processor = None
_profiles: list[dict[str, Any]] = []
_embeddings: np.ndarray | None = None

PKL_PATH = Path(__file__).parent.parent / "data" / "cat_profiles.pkl"
MODEL_NAME = "openai/clip-vit-large-patch14"  # Using available CLIP model
CONFIDENCE_THRESHOLD = 0.70


def _load_model():
    global _model, _processor
    if _model is not None:
        return
    from transformers import AutoProcessor, AutoModel
    import torch

    _processor = AutoProcessor.from_pretrained(MODEL_NAME)
    _model = AutoModel.from_pretrained(MODEL_NAME)
    _model.eval()


def _load_profiles():
    global _profiles, _embeddings
    if _embeddings is not None:
        return
    if not PKL_PATH.exists():
        _profiles = []
        _embeddings = np.empty((0, 0), dtype=np.float32)
        return
    with open(PKL_PATH, "rb") as f:
        data = pickle.load(f)
    _profiles = data["profiles"]
    _embeddings = np.array(data["embeddings"], dtype=np.float32)


def embed_image(image_bytes: bytes) -> np.ndarray:
    """Return a normalized L2 embedding vector for the given image bytes."""
    import torch

    _load_model()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    inputs = _processor(images=image, return_tensors="pt")
    with torch.no_grad():
        features = _model.get_image_features(**inputs)
    vec = features[0].cpu().numpy()
    vec = vec / (np.linalg.norm(vec) + 1e-8)
    return vec


def find_best_match(image_bytes: bytes) -> dict[str, Any]:
    """Compare uploaded image against the pkl vector DB.

    Returns the top matching cat profile + confidence, or no_match=True.
    """
    _load_profiles()

    query_vec = embed_image(image_bytes)

    if _embeddings is None or len(_embeddings) == 0:
        return {"no_match": True, "match": None}

    # Cosine similarity (vectors already L2-normalised)
    scores = _embeddings @ query_vec
    best_idx = int(np.argmax(scores))
    confidence = float(scores[best_idx])

    if confidence < CONFIDENCE_THRESHOLD:
        return {"no_match": True, "match": None, "confidence": confidence}

    cat = dict(_profiles[best_idx])
    cat["confidence"] = round(confidence, 4)
    return {"no_match": False, "match": cat}
