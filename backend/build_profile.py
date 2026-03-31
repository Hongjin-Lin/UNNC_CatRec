"""Build cats.db (SQLite) from cats.json + campus_cats_library images.

Usage:
    cd backend
    python build_profile.py

Outputs:
    data/cats.db
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent.parent
CATS_JSON = ROOT / "cats.json"
LIBRARY_DIR = ROOT / "campus_cats_library"
DB_PATH = Path(__file__).parent / "data" / "cats.db"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# Keep these cats pinned to the top in "default" ordering.
DEFAULT_NAME_ORDER = ["橙子", "森森", "馒头", "黄苹果", "小话痨", "小话唠"]
DEFAULT_RANK = {name: idx for idx, name in enumerate(DEFAULT_NAME_ORDER, start=1)}


def first_image_url(name: str) -> str | None:
    """Return the /static/cats/<name>/<file> URL for the first image found."""
    cat_dir = LIBRARY_DIR / name
    if not cat_dir.exists():
        return None
    for p in sorted(cat_dir.iterdir()):
        if p.suffix.lower() in IMAGE_EXTENSIONS:
            return f"/static/cats/{quote(name)}/{quote(p.name)}"
    return None


def to_bool(value: object) -> int:
    if isinstance(value, bool):
        return 1 if value else 0
    if value is None:
        return 0
    text = str(value).strip().lower()
    return 1 if text in {"1", "true", "yes", "y", "是", "已绝育"} else 0


def to_int(value: object, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(str(value)))
    except Exception:
        return default


def to_float(value: object) -> float | None:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except Exception:
        return None


def rebuild_table(conn: sqlite3.Connection):
    conn.execute("DROP TABLE IF EXISTS cats")
    conn.execute("""
        CREATE TABLE cats (
            id               INTEGER PRIMARY KEY,
            name             TEXT NOT NULL,
            species          TEXT,
            breed            TEXT,
            color            TEXT,
            gender           TEXT,
            estimated_age    REAL,
            weight           REAL,
            location         TEXT,
            status           TEXT,
            personality      TEXT,
            tnr_status       INTEGER DEFAULT 0,
            is_friendly      TEXT,
            notes            TEXT,
            image_url        TEXT,
            click_count      INTEGER DEFAULT 0,
            likes_count      INTEGER DEFAULT 0,
            comments_count   INTEGER DEFAULT 0,
            favorites_count  INTEGER DEFAULT 0,
            default_rank     INTEGER DEFAULT 9999
        )
    """)
    conn.commit()


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(CATS_JSON, encoding="utf-8") as f:
        cats = json.load(f)["list"]

    print(f"Found {len(cats)} cats in cats.json")

    conn = sqlite3.connect(DB_PATH)
    rebuild_table(conn)

    inserted = 0
    for cat in cats:
        name = (cat.get("Name") or "").strip()
        if not name:
            continue

        personality_parts: list[str] = []
        if cat.get("Is_friendly") == "是":
            personality_parts.append("亲人")
        elif cat.get("Is_friendly") == "否":
            personality_parts.append("怕生")

        default_rank = DEFAULT_RANK.get(name, 9999 + to_int(cat.get("id"), 0))

        click_count = to_int(cat.get("Click_count", cat.get("click_count", 0)), 0)
        likes_count = to_int(cat.get("Likes_count", cat.get("likes_count", 0)), 0)
        comments_count = to_int(cat.get("Comments_count", cat.get("comments_count", 0)), 0)
        favorites_count = to_int(cat.get("Favorites_count", cat.get("favorites_count", 0)), 0)

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
                cat["id"],
                name,
                cat.get("Species") or "",
                cat.get("Breed") or "",
                cat.get("Color") or "",
                cat.get("Gender") or "未知",
                to_float(cat.get("Estimated_Age")),
                to_float(cat.get("Weight")),
                cat.get("Discovery_location") or "",
                cat.get("Current_status") or "",
                ",".join(personality_parts),
                to_bool(cat.get("Is_neutered")),
                cat.get("Is_friendly") or "",
                cat.get("Description") or "",
                first_image_url(name),
                click_count,
                likes_count,
                comments_count,
                favorites_count,
                default_rank,
            ),
        )
        inserted += 1

    conn.commit()
    conn.close()
    print(f"Done. {inserted} cats written to {DB_PATH}")


if __name__ == "__main__":
    main()
