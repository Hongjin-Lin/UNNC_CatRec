from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from services.nocodb_service import create_cat
from services.identify_service import embed_image

router = APIRouter()


@router.post("/add")
async def add_cat(
    name: str = Form(...),
    location: str = Form(...),
    personality: str = Form(""),
    tnr_status: bool = Form(False),
    notes: Optional[str] = Form(None),
    image: UploadFile = File(...),
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = await image.read()
    embedding = embed_image(image_bytes)

    personality_list = [p.strip() for p in personality.split(",") if p.strip()]

    cat_data = {
        "name": name,
        "location": location,
        "personality": personality_list,
        "tnr_status": tnr_status,
        "notes": notes,
        "embedding": embedding.tolist(),
    }

    result = await create_cat(cat_data, image_bytes, image.filename)
    return {"id": result["id"], "status": "created"}
