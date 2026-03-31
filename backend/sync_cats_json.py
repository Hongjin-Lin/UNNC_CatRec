"""Sync cats.json from NocoDB records API.

Usage:
    cd backend
    python sync_cats_json.py

Required env vars:
    NOCODB_BASE_URL
    NOCODB_API_TOKEN
    NOCODB_TABLE_ID

Output:
    ../cats.json
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent.parent
OUT_PATH = ROOT / "cats.json"


def main() -> None:
    base_url = os.getenv("NOCODB_BASE_URL", "").rstrip("/")
    table_id = os.getenv("NOCODB_TABLE_ID", "")
    token = os.getenv("NOCODB_API_TOKEN", "")

    if not base_url or not table_id or not token:
        raise RuntimeError(
            "Missing env. Please set NOCODB_BASE_URL, NOCODB_TABLE_ID, NOCODB_API_TOKEN"
        )

    headers = {"xc-auth": token}

    all_rows: list[dict] = []
    offset = 0
    limit = 200

    while True:
        url = f"{base_url}/api/v1/db/data/noco/{table_id}"
        resp = requests.get(url, headers=headers, params={"offset": offset, "limit": limit}, timeout=20)
        resp.raise_for_status()
        data = resp.json()

        rows = data.get("list", [])
        if not rows:
            break

        all_rows.extend(rows)
        if len(rows) < limit:
            break
        offset += limit

    payload = {"list": all_rows}
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Synced {len(all_rows)} rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
