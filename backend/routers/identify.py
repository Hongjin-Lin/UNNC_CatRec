import sqlite3
import time
import asyncio
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

    start_time = time.time()
    
    image_bytes = await image.read()
    read_img_time = time.time()
    print(f"[Profiling] Time to read image bytes: {read_img_time - start_time:.4f} seconds")

    # 使用 asyncio.to_thread 防止阻塞主事件循环
    result = await asyncio.to_thread(find_best_match, image_bytes)
    inference_time = time.time()
    print(f"[Profiling] Time for AI inference (find_best_match): {inference_time - read_img_time:.4f} seconds")

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

    total_time = time.time()
    print(f"[Profiling] Time for DB enrichment: {total_time - inference_time:.4f} seconds")
    print(f"[Profiling] TOTAL server processing time: {total_time - start_time:.4f} seconds")

    return result
