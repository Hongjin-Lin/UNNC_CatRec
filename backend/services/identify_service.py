"""Animal identification inference service.

Model: AvitoTech/DINO-v2-small-for-animal-identification
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
_profiles: list[dict[str, Any]] = []
_embeddings: np.ndarray | None = None

PKL_PATH = Path(__file__).parent.parent / "data" / "cat_profiles.pkl"
BASE_CKP = "facebook/dinov2-small"
AVITO_REPO = "AvitoTech/DINO-v2-small-for-animal-identification"
AVITO_FILE = "model.safetensors"
LOCAL_MODEL_DIR = Path(__file__).parent.parent.parent / "model_save"
CONFIDENCE_THRESHOLD = 0.70


def _load_model():
    global _model
    if _model is not None:
        return
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

    model = Model()

    local_avito = LOCAL_MODEL_DIR / AVITO_FILE
    if local_avito.exists():
        weights_path = str(local_avito)
    else:
        weights_path = hf_hub_download(repo_id=AVITO_REPO, filename=AVITO_FILE)

    state_dict = safetensors.torch.load_file(weights_path)
    model.load_state_dict(state_dict, strict=False)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    _model = model.to(device).eval()


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
    import torch.nn.functional as F

    _load_model()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    with torch.no_grad():
        feat = _model([image])
        feat = F.normalize(feat, dim=1)
    return feat[0].cpu().numpy().astype(np.float32)


def find_best_match(image_bytes: bytes) -> dict[str, Any]:
    """Compare uploaded image against the pkl vector DB.

    Returns top-3 matching cat profiles + confidence, or no_match=True.
    """
    _load_profiles()

    query_vec = embed_image(image_bytes)

    if _embeddings is None or len(_embeddings) == 0:
        return {"no_match": True, "matches": []}

    scores = _embeddings @ query_vec
    top_k = min(3, len(_profiles))
    top_indices = np.argsort(scores)[::-1][:top_k]

    matches = []
    for idx in top_indices:
        cat = dict(_profiles[idx])
        cat["confidence"] = round(float(scores[idx]), 4)
        matches.append(cat)

    if matches[0]["confidence"] < CONFIDENCE_THRESHOLD:
        return {"no_match": True, "matches": matches}

    return {"no_match": False, "matches": matches}
