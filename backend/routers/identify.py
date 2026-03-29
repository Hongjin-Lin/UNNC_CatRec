import sqlite3
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.identify_service import find_best_match

router = APIRouter()
DB_PATH = Path(__file__).parent.parent / "data" / "cats.db"

@router.post("")
@router.post("/")
async def identify_cat(image: UploadFile = File(...)):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = await image.read()
    result = find_best_match(image_bytes)
    
    # Enrich matches with data from SQLite DB
    if not result.get("no_match") and DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        
        for match in result.get("matches", []):
            cat_name = match.get("name")
            if cat_name:
                row = conn.execute(
                    "SELECT id, location, personality, tnr_status, notes FROM cats WHERE name = ?", 
                    (cat_name,)
                ).fetchone()
                
                if row:
                    match["id"] = str(row["id"])
                    match["location"] = row["location"]
                    # Personality comes as comma-separated string, frontend expects an array (or handles it strings?)
                    # Frontend identify/index.vue uses "cat.personality?.length" with v-for="t in cat.personality"
                    # So we should split it into a list
                    if row["personality"]:
                        match["personality"] = [p.strip() for p in row["personality"].split(",") if p.strip()]
                    else:
                        match["personality"] = []
                    match["tnr_status"] = bool(row["tnr_status"])
                    match["notes"] = row["notes"]
        conn.close()

    return result
