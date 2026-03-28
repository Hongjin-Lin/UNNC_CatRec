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
def map_data():
    conn = _get_db()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT name, location FROM cats").fetchall()
    conn.close()

    grouped = {}
    for row in rows:
        tag = row["location"] or "unknown"
        grouped.setdefault(tag, []).append(row["name"])

    # Hardcoded mapping from location tag -> GPS coords for the UNNC campus.
    # Base mapping around center: 29.80002, 121.56351
    LOCATION_COORDS = {
        "23": (29.8035, 121.5620),
        "22": (29.8028, 121.5625),
        "17": (29.8040, 121.5610),
        "18": (29.8045, 121.5615),
        "DB": (29.7990, 121.5635),
        "Trent": (29.8000, 121.5645),
        "诺丁桥": (29.7985, 121.5625),
        "IAMET": (29.7975, 121.5655),
        "图书馆": (29.8015, 121.5640),
        "垃圾站": (29.8055, 121.5630),
        "宿舍": (29.8030, 121.5615),
        "行政楼": (29.8005, 121.5655),
        "生活区": (29.8025, 121.5610),
    }

    hotspots = []
    for tag, names in grouped.items():
        # Match substring to find approximate coords
        coords = None
        for key, value in LOCATION_COORDS.items():
            if key in tag:
                coords = value
                break
        
        if coords:
            hotspots.append({"tag": tag, "lat": coords[0], "lng": coords[1], "cats": names})
        else:
            hotspots.append({"tag": tag, "lat": None, "lng": None, "cats": names})
    
    return {"hotspots": hotspots}
