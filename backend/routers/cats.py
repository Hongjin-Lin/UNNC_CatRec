from fastapi import APIRouter, HTTPException
from services.nocodb_service import get_all_cats, get_map_data

router = APIRouter()


@router.get("")
async def list_cats():
  @router.get("")
  async def list_cats():
      return {"cats": [
          {"id": "1", "Name": "橘猫小花", "Location": "#23", "Personality": "亲人,爱撒娇", "TNR_Status": True},
          {"id": "2", "Name": "黑猫阿墨", "Location": "#01", "Personality": "怕生", "TNR_Status": False},
      ]}

@router.get("/map-data")
async def map_data():
    hotspots = await get_map_data()
    return {"hotspots": hotspots}
