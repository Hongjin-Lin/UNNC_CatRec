from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

from services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["Users"])

class UserProfileUpdate(BaseModel):
    username: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]

@router.get("/{user_id}", summary="Get or create a user profile")
async def get_user_profile(user_id: str):
    """
    Given a user ID (e.g., from WeChat OpenID auth), return their profile.
    If they don't exist, a new profile is created with a random cat-themed username.
    """
    try:
        user_data = UserService.get_or_create_user(user_id)
        return {"status": "success", "data": user_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{user_id}", summary="Update user profile")
async def update_user_profile(user_id: str, payload: UserProfileUpdate):
    """
    Update standard user fields like username (if they want to override the random one).
    """
    try:
        update_data = payload.dict(exclude_unset=True)
        # TODO: Implement concrete call to update logic
        # updated = UserService.update_user_profile(user_id, update_data)
        return {"status": "success", "message": "Profile updated successfully.", "updates": update_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
