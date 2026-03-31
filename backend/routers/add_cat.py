import os
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from services.local_cat_service import create_local_cat
from services.nocodb_service import create_cat as create_cat_nocodb

router = APIRouter()


@router.post("/add")
@router.post("/add/")
async def add_cat(
    name: str = Form(...),
    location: str = Form(""),
    personality: str = Form(""),
    species: str = Form("猫"),
    breed: str = Form(""),
    color: str = Form(""),
    gender: str = Form("未知"),
    estimated_age: Optional[str] = Form(None),
    weight: Optional[str] = Form(None),
    status: str = Form(""),
    is_friendly: str = Form(""),
    tnr_status: bool = Form(False),
    notes: Optional[str] = Form(None),
    image: UploadFile = File(...),
):
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = await image.read()

    cat_data = {
        "name": name,
        "location": location,
        "personality": personality,
        "species": species,
        "breed": breed,
        "color": color,
        "gender": gender,
        "estimated_age": estimated_age,
        "weight": weight,
        "status": status,
        "is_friendly": is_friendly,
        "tnr_status": tnr_status,
        "notes": notes,
    }

    # 1) Primary write: local library + sqlite + cats.json
    result = create_local_cat(cat_data, image_bytes, image.filename)

    # 2) Best-effort sync to NocoDB (optional, won't block local success)
    if os.getenv("NOCODB_BASE_URL") and os.getenv("NOCODB_TABLE_ID") and os.getenv("NOCODB_API_TOKEN"):
        try:
            await create_cat_nocodb(
                {
                    "name": name,
                    "location": location,
                    "personality": [p.strip() for p in personality.split(",") if p.strip()],
                    "tnr_status": tnr_status,
                    "notes": notes,
                },
                image_bytes,
                image.filename,
            )
        except Exception as exc:
            # Local success should not be rolled back by remote sync failure.
            print(f"[add_cat] NocoDB sync skipped/failed: {exc}")

    return {"id": result["id"], "status": "created"}
