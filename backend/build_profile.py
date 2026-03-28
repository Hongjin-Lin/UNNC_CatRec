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


def first_image_url(name: str) -> str | None:
    """Return the /static/cats/<name>/<file> URL for the first image found."""
    cat_dir = LIBRARY_DIR / name
    if not cat_dir.exists():
        return None
    for p in sorted(cat_dir.iterdir()):
        if p.suffix.lower() in IMAGE_EXTENSIONS:
            return f"/static/cats/{quote(name)}/{quote(p.name)}"
    return None


def create_table(conn: sqlite3.Connection):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cats (
            id          INTEGER PRIMARY KEY,
            name        TEXT NOT NULL,
            location    TEXT,
            personality TEXT,
            tnr_status  INTEGER DEFAULT 0,
            notes       TEXT,
            image_url   TEXT
        )
    """)
    conn.commit()


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(CATS_JSON, encoding="utf-8") as f:
        cats = json.load(f)["list"]

    print(f"Found {len(cats)} cats in cats.json")

    conn = sqlite3.connect(DB_PATH)
    create_table(conn)
    conn.execute("DELETE FROM cats")  # full rebuild

    inserted = 0
    for cat in cats:
        name = (cat.get("Name") or "").strip()
        if not name:
            continue

        personality_parts = []
        if cat.get("Is_friendly") == "是":
            personality_parts.append("亲人")
        elif cat.get("Is_friendly") == "否":
            personality_parts.append("怕生")

        conn.execute(
            """
            INSERT INTO cats (id, name, location, personality, tnr_status, notes, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                cat["id"],
                name,
                cat.get("Discovery_location") or "",
                ",".join(personality_parts),
                1 if cat.get("Is_neutered") else 0,
                cat.get("Description") or "",
                first_image_url(name),
            ),
        )
        inserted += 1

    conn.commit()
    conn.close()
    print(f"Done. {inserted} cats written to {DB_PATH}")


if __name__ == "__main__":
    main()
