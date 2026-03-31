# Cat Data Pipeline

This project now has a clear 3-step data pipeline for cat metadata + photos:

1. Sync metadata from NocoDB into `cats.json`
   - Script: `backend/sync_cats_json.py`
   - Output: `cats.json`

2. Download cat photos from the JSON attachment paths
   - Script: `backend/profile_script.py`
   - Input: `cats.json`
   - Output: `campus_cats_library/<cat_name>/*`

3. Build SQLite database for backend APIs
   - Script: `backend/build_profile.py`
   - Inputs: `cats.json` + `campus_cats_library`
   - Output: `backend/data/cats.db`

## Why this split exists

- `sync_cats_json.py` is the only script that talks to NocoDB and pulls records.
- `profile_script.py` does not fetch records from NocoDB. It only reads local `cats.json` and downloads media files.
- `build_profile.py` maps selected attributes from JSON to SQLite fields used by frontend pages.

## Typical refresh workflow

```bash
cd backend
python sync_cats_json.py
python profile_script.py
python build_profile.py
```
