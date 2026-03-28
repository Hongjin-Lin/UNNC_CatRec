"""NocoDB REST API client."""
from __future__ import annotations

import os
from typing import Any

import httpx

BASE_URL = os.getenv("NOCODB_BASE_URL", "")
API_TOKEN = os.getenv("NOCODB_API_TOKEN", "")
TABLE_ID = os.getenv("NOCODB_TABLE_ID", "")

# Hardcoded mapping from location tag → GPS coords for the UNNC campus.
# Extend this dict as new locations are discovered.
LOCATION_COORDS: dict[str, tuple[float, float]] = {
    "#23": (31.8320, 121.6830),
    "#01": (31.8310, 121.6820),
    "#05": (31.8315, 121.6840),
}


def _headers() -> dict[str, str]:
    return {"xc-auth": API_TOKEN, "Content-Type": "application/json"}


async def get_all_cats() -> list[dict[str, Any]]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE_URL}/api/v1/db/data/noco/{TABLE_ID}",
            headers=_headers(),
            params={"limit": 200},
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("list", [])


async def create_cat(
    cat_data: dict[str, Any],
    image_bytes: bytes,
    filename: str | None,
) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        # 1. Create record
        payload = {
            "Name": cat_data["name"],
            "Location": cat_data["location"],
            "Personality": ",".join(cat_data.get("personality", [])),
            "TNR_Status": cat_data["tnr_status"],
            "Notes": cat_data.get("notes") or "",
        }
        resp = await client.post(
            f"{BASE_URL}/api/v1/db/data/noco/{TABLE_ID}",
            headers=_headers(),
            json=payload,
        )
        resp.raise_for_status()
        record = resp.json()
        row_id = record["id"]

        # 2. Upload image attachment
        files = {"file": (filename or "photo.jpg", image_bytes)}
        attach_resp = await client.post(
            f"{BASE_URL}/api/v1/db/data/noco/{TABLE_ID}/{row_id}/attachments",
            headers={"xc-auth": API_TOKEN},
            files=files,
        )
        attach_resp.raise_for_status()

        return {"id": str(row_id)}


async def get_map_data() -> list[dict[str, Any]]:
    cats = await get_all_cats()

    grouped: dict[str, list[str]] = {}
    for cat in cats:
        tag = cat.get("Location", "unknown")
        grouped.setdefault(tag, []).append(cat.get("Name", "?"))

    hotspots = []
    for tag, names in grouped.items():
        coords = LOCATION_COORDS.get(tag)
        if coords:
            hotspots.append({"tag": tag, "lat": coords[0], "lng": coords[1], "cats": names})
        else:
            # Unknown location — still include with null coords so frontend can show a list
            hotspots.append({"tag": tag, "lat": None, "lng": None, "cats": names})
    return hotspots
