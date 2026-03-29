import sqlite3
from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter()

DB_PATH = Path(__file__).parent.parent / "data" / "cats.db"
LIBRARY_PATH = Path(__file__).parent.parent.parent / "campus_cats_library"
IMAGE_EXTS = {".jpeg", ".jpg", ".png", ".webp"}


def _get_db():
    if not DB_PATH.exists():
        raise HTTPException(status_code=503, detail="cats.db not found — run build_profile.py first")
    return sqlite3.connect(DB_PATH)


def _get_photos(cat_name: str) -> list[str]:
    """Return sorted list of image URLs for a cat by scanning the library folder."""
    folder = LIBRARY_PATH / cat_name
    if not folder.exists():
        return []
    files = sorted(
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTS
    )
    return [f"/static/cats/{cat_name}/{f.name}" for f in files]


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


# Must be registered BEFORE /{cat_id} to avoid being matched as a cat id
@router.get("/map-data")
@router.get("/map-data/")
def map_data():
    conn = _get_db()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT name, location FROM cats").fetchall()
    conn.close()

    grouped = {}
    for row in rows:
        tag = row["location"] or "unknown"
        grouped.setdefault(tag, []).append(row["name"])

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


@router.get("/{cat_id}")
def get_cat(cat_id: str):
    conn = _get_db()
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT id, name, location, personality, tnr_status, notes, image_url FROM cats WHERE id = ?",
        (cat_id,)
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Cat not found")
    photos = _get_photos(row["name"])
    return {
        "id": str(row["id"]),
        "Name": row["name"],
        "Location": row["location"],
        "Personality": row["personality"],
        "TNR_Status": bool(row["tnr_status"]),
        "Notes": row["notes"],
        "image_url": row["image_url"],
        "photos": photos,
    }
