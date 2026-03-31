import random
import uuid
from typing import Optional, Dict, Any
from datetime import datetime

# Adjectives and nouns for generating default random usernames
ADJECTIVES = ["爱喵的", "贪吃的", "慵懒的", "神秘的", "调皮的", "高冷的", "友善的", "好奇的"]
NOUNS = ["同学", "两脚兽", "铲屎官", "过客", "黑猫", "橘猫", "志愿者", "喵星人"]

def generate_random_username() -> str:
    """Generate a random default cat-themed username."""
    adj = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    return f"{adj}{noun}_{random.randint(1000, 9999)}"

def create_new_user(openid: Optional[str] = None) -> Dict[str, Any]:
    """
    Standard function to generate a new user document/record.
    Includes default username generation and reserved stat fields.
    """
    user_id = openid if openid else str(uuid.uuid4())
    
    return {
        "id": user_id,
        "username": generate_random_username(),
        "avatar_url": "",  # Default avatar could be set here
        "role": "user",
        "bio": "这个人很懒，什么都没写（除了吸猫）。",
        "contact": "",
        "stats": {
            "following_count": 0,
            "followers_count": 0,
            "likes_received": 0
        },
        "created_at": datetime.utcnow().isoformat(),
        "last_login": datetime.utcnow().isoformat()
    }

class UserService:
    """
    Service class logic to handle User accounts.
    Integrates with NocoDB eventually.
    """
    @staticmethod
    def get_or_create_user(user_id: str) -> Dict[str, Any]:
        """
        Mock implementation: 
        In production, query NocoDB by user_id. If not found, call create_new_user() 
        and save to NocoDB 'Users' table.
        """
        # TODO: Implement NocoDB fetching logic
        # e.g., result = nocodb_service.fetch_record("Users", user_id)
        # if result: return result
        
        # Fallback for new user creation
        new_user = create_new_user(user_id)
        # TODO: nocodb_service.insert_record("Users", new_user)
        return new_user

    @staticmethod
    def update_user_profile(user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user fields (e.g. they changed their randomly generated username).
        """
        # TODO: Implement NocoDB update logic
        pass

