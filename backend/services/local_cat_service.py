from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote

BACKEND_DIR = Path(__file__).resolve().parent.parent
ROOT = BACKEND_DIR.parent
DB_PATH = BACKEND_DIR / "data" / "cats.db"
LIBRARY_DIR = ROOT / "campus_cats_library"
CATS_JSON = ROOT / "cats.json"

DEFAULT_NAME_ORDER = ["橙子", "森森", "馒头", "黄苹果", "小话痨", "小话唠"]
DEFAULT_RANK = {name: idx for idx, name in enumerate(DEFAULT_NAME_ORDER, start=1)}


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except Exception:
        return None


def _sanitize_name(name: str) -> str:
    return name.replace("/", "_").replace("\\", "_").strip()


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

    for idx, cat_name in enumerate(DEFAULT_NAME_ORDER, start=1):
        conn.execute("UPDATE cats SET default_rank = ? WHERE name = ?", (idx, cat_name))
    conn.commit()


def _next_id(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT COALESCE(MAX(id), 0) + 1 AS next_id FROM cats").fetchone()
    return int(row[0])


def _save_image(name: str, image_bytes: bytes, filename: str | None) -> tuple[str, str]:
    safe_name = _sanitize_name(name)
    ext = Path(filename or "photo.jpg").suffix.lower() or ".jpg"
    if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
        ext = ".jpg"

    cat_dir = LIBRARY_DIR / safe_name
    cat_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_name = f"{safe_name}_user_{stamp}{ext}"
    image_path = cat_dir / image_name
    image_path.write_bytes(image_bytes)

    image_url = f"/static/cats/{quote(safe_name)}/{quote(image_name)}"
    return safe_name, image_url


def _append_to_cats_json(payload: dict[str, Any]) -> None:
    if CATS_JSON.exists():
        try:
            data = json.loads(CATS_JSON.read_text(encoding="utf-8"))
        except Exception:
            data = {"list": []}
    else:
        data = {"list": []}

    if isinstance(data, list):
        cat_list = data
    else:
        cat_list = data.get("list", [])

    cat_list.append(payload)

    if isinstance(data, list):
        out = cat_list
    else:
        data["list"] = cat_list
        out = data

    CATS_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")


def create_local_cat(cat_data: dict[str, Any], image_bytes: bytes, filename: str | None) -> dict[str, str]:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    LIBRARY_DIR.mkdir(parents=True, exist_ok=True)

    safe_name, image_url = _save_image(str(cat_data.get("name", "")), image_bytes, filename)

    conn = sqlite3.connect(DB_PATH)
    _ensure_schema(conn)
    new_id = _next_id(conn)

    default_rank = DEFAULT_RANK.get(safe_name, 9999 + new_id)

    conn.execute(
        """
        INSERT INTO cats (
            id, name, species, breed, color, gender, estimated_age, weight,
            location, status, personality, tnr_status, is_friendly, notes, image_url,
            click_count, likes_count, comments_count, favorites_count, default_rank
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            new_id,
            safe_name,
            cat_data.get("species", "猫") or "猫",
            cat_data.get("breed", "") or "",
            cat_data.get("color", "") or "",
            cat_data.get("gender", "未知") or "未知",
            _to_float(cat_data.get("estimated_age")),
            _to_float(cat_data.get("weight")),
            cat_data.get("location", "") or "",
            cat_data.get("status", "") or "",
            cat_data.get("personality", "") or "",
            1 if bool(cat_data.get("tnr_status")) else 0,
            cat_data.get("is_friendly", "") or "",
            cat_data.get("notes", "") or "",
            image_url,
            0,
            0,
            0,
            0,
            default_rank,
        ),
    )
    conn.commit()
    conn.close()

    _append_to_cats_json(
        {
            "id": new_id,
            "Name": safe_name,
            "Species": cat_data.get("species", "猫") or "猫",
            "Breed": cat_data.get("breed", "") or "",
            "Color": cat_data.get("color", "") or "",
            "Gender": cat_data.get("gender", "未知") or "未知",
            "Estimated_Age": _to_float(cat_data.get("estimated_age")),
            "Weight": _to_float(cat_data.get("weight")),
            "Is_neutered": bool(cat_data.get("tnr_status")),
            "Is_friendly": cat_data.get("is_friendly", "") or "",
            "Discovery_location": cat_data.get("location", "") or "",
            "Current_status": cat_data.get("status", "") or "",
            "Description": cat_data.get("notes", "") or "",
            "Photos": [],
        }
    )

    return {"id": str(new_id)}
