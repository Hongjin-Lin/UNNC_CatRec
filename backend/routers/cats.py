import sqlite3
from pathlib import Path
from fastapi import APIRouter, HTTPException
from services.nocodb_service import get_map_data

router = APIRouter()

DB_PATH = Path(__file__).parent.parent / "data" / "cats.db"


def _get_db():
    if not DB_PATH.exists():
        raise HTTPException(status_code=503, detail="cats.db not found — run build_profile.py first")
    return sqlite3.connect(DB_PATH)


@router.get("/")
def list_cats():
    conn = _get_db()
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, name, location, personality, tnr_status, notes, image_url FROM cats"
    ).fetchall()
    conn.close()
    cats = [
        {
            "id": str(row["id"]),
            "Name": row["name"],
            "Location": row["location"],
            "Personality": row["personality"],
            "TNR_Status": bool(row["tnr_status"]),
            "Notes": row["notes"],
            "image_url": row["image_url"],
        }
        for row in rows
    ]
    return {"cats": cats}


@router.get("/map-data")
async def map_data():
    hotspots = await get_map_data()
    return {"hotspots": hotspots}
