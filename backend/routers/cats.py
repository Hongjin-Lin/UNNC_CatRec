import sqlite3
from pathlib import Path
from fastapi import APIRouter, HTTPException
from typing import Any

router = APIRouter()

DB_PATH = Path(__file__).parent.parent / "data" / "cats.db"
LIBRARY_PATH = Path(__file__).parent.parent.parent / "campus_cats_library"
IMAGE_EXTS = {".jpeg", ".jpg", ".png", ".webp"}
DEFAULT_NAME_ORDER = ["橙子", "森森", "馒头", "黄苹果", "小话痨", "小话唠"]
DEFAULT_RANK = {name: idx for idx, name in enumerate(DEFAULT_NAME_ORDER, start=1)}


def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    return text in {"1", "true", "yes", "y", "是", "已绝育"}


def _to_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(str(value)))
    except Exception:
        return default


def _row_get(row: sqlite3.Row, key: str, default: Any = None) -> Any:
    return row[key] if key in row.keys() else default


def _ensure_schema(conn: sqlite3.Connection) -> None:
    columns = {r[1] for r in conn.execute("PRAGMA table_info(cats)").fetchall()}
    desired_columns = {
        "species": "TEXT",
        "breed": "TEXT",
        "color": "TEXT",
        "gender": "TEXT",
        "estimated_age": "REAL",
        "weight": "REAL",
        "status": "TEXT",
        "is_friendly": "TEXT",
        "click_count": "INTEGER DEFAULT 0",
        "likes_count": "INTEGER DEFAULT 0",
        "comments_count": "INTEGER DEFAULT 0",
        "favorites_count": "INTEGER DEFAULT 0",
        "default_rank": "INTEGER DEFAULT 9999",
    }
    for col, ddl in desired_columns.items():
        if col not in columns:
            conn.execute(f"ALTER TABLE cats ADD COLUMN {col} {ddl}")

    # Ensure pinned default order is always respected.
    for idx, name in enumerate(DEFAULT_NAME_ORDER, start=1):
        conn.execute("UPDATE cats SET default_rank = ? WHERE name = ?", (idx, name))

    conn.commit()


def _get_db():
    if not DB_PATH.exists():
        raise HTTPException(status_code=503, detail="cats.db not found — run build_profile.py first")
    conn = sqlite3.connect(DB_PATH)
    _ensure_schema(conn)
    return conn


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


def _cat_payload(row: sqlite3.Row) -> dict[str, Any]:
    name = _row_get(row, "name", "")
    default_rank = _to_int(_row_get(row, "default_rank", None), DEFAULT_RANK.get(name, 9999))

    click_count = _to_int(_row_get(row, "click_count", 0), 0)
    likes_count = _to_int(_row_get(row, "likes_count", 0), 0)
    comments_count = _to_int(_row_get(row, "comments_count", 0), 0)
    favorites_count = _to_int(_row_get(row, "favorites_count", 0), 0)

    # Weighted heat score used by "hot" sorting on frontend/backed params.
    heat_score = click_count * 0.4 + likes_count * 0.4 + comments_count * 0.2

    return {
        "id": str(_row_get(row, "id", "")),
        "Name": name,
        "Species": _row_get(row, "species", "") or "",
        "Breed": _row_get(row, "breed", "") or "",
        "Color": _row_get(row, "color", "") or "",
        "Gender": _row_get(row, "gender", "未知") or "未知",
        "Estimated_Age": _row_get(row, "estimated_age", None),
        "Weight": _row_get(row, "weight", None),
        "Location": _row_get(row, "location", "") or "",
        "Current_status": _row_get(row, "status", "") or "",
        "Personality": _row_get(row, "personality", "") or "",
        "TNR_Status": _to_bool(_row_get(row, "tnr_status", 0)),
        "Is_friendly": _row_get(row, "is_friendly", "") or "",
        "Notes": _row_get(row, "notes", "") or "",
        "image_url": _row_get(row, "image_url", "") or "",
        "click_count": click_count,
        "likes_count": likes_count,
        "comments_count": comments_count,
        "favorites_count": favorites_count,
        "default_rank": default_rank,
        "heat_score": round(heat_score, 2),
    }


def _category_key(cat: dict[str, Any]) -> str:
    breed = (cat.get("Breed") or "").strip()
    species = (cat.get("Species") or "").strip()
    return breed or species or "未知"


def _apply_filters(
    cats: list[dict[str, Any]],
    gender: str | None,
    neutered: str | None,
    status: str | None,
    category: str | None,
) -> list[dict[str, Any]]:
    out = cats

    if gender and gender not in {"all", "不限"}:
        out = [c for c in out if (c.get("Gender") or "") == gender]

    if neutered and neutered not in {"all", "不限"}:
        target = neutered in {"yes", "1", "true", "是", "已绝育"}
        out = [c for c in out if bool(c.get("TNR_Status")) == target]

    if status and status not in {"all", "不限"}:
        out = [c for c in out if (c.get("Current_status") or "") == status]

    if category and category not in {"all", "不限"}:
        out = [c for c in out if category in _category_key(c)]

    return out


def _apply_sort(cats: list[dict[str, Any]], sort: str) -> list[dict[str, Any]]:
    if sort == "hot":
        return sorted(cats, key=lambda c: (c.get("heat_score", 0), c.get("likes_count", 0), c.get("click_count", 0)), reverse=True)
    if sort == "category":
        return sorted(cats, key=lambda c: (_category_key(c), c.get("default_rank", 9999), c.get("id", "")))
    # default
    return sorted(cats, key=lambda c: (c.get("default_rank", 9999), c.get("id", "")))


@router.get("/")
def list_cats(
    sort: str = "default",
    gender: str | None = None,
    neutered: str | None = None,
    status: str | None = None,
    category: str | None = None,
):
    conn = _get_db()
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM cats").fetchall()
    conn.close()

    cats = [_cat_payload(row) for row in rows]
    cats = _apply_filters(cats, gender=gender, neutered=neutered, status=status, category=category)
    cats = _apply_sort(cats, sort=sort)

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
    row = conn.execute("SELECT * FROM cats WHERE id = ?", (cat_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Cat not found")
    payload = _cat_payload(row)
    payload["photos"] = _get_photos(payload["Name"])
    return payload


@router.post("/{cat_id}/click")
def increment_click(cat_id: str):
    conn = _get_db()
    conn.row_factory = sqlite3.Row
    existing = conn.execute("SELECT id FROM cats WHERE id = ?", (cat_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Cat not found")

    conn.execute(
        "UPDATE cats SET click_count = COALESCE(click_count, 0) + 1 WHERE id = ?",
        (cat_id,),
    )
    conn.commit()

    row = conn.execute("SELECT click_count FROM cats WHERE id = ?", (cat_id,)).fetchone()
    conn.close()
    return {"id": str(cat_id), "click_count": _to_int(row["click_count"], 0)}
