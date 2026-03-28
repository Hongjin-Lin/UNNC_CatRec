from fastapi import APIRouter, UploadFile, File, HTTPException
from services.identify_service import find_best_match

router = APIRouter()


@router.post("")
async def identify_cat(image: UploadFile = File(...)):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = await image.read()
    result = find_best_match(image_bytes)
    return result
