from src.database import db
from src.schemas import UserIn
from datetime import datetime, timezone
from uuid import uuid4
from src.auth import create_jwt_token
from passlib.hash import bcrypt

async def get_user_by_email(email: str):
    return await db.users.find_one({"email": email})

async def create_user(user: UserIn):
    now = datetime.now(timezone.utc).isoformat()
    uid = str(uuid4())

    token = create_jwt_token({"id": uid, "email": user.email})
    
    user_dict = user.model_dump()
    user_dict.update({
        "id": uid,
        "created": now,
        "modified": now,
        "last_login": now,
        "token": token,
        "isactive": True,
        "password": bcrypt.hash(user.password)
    })
    
    await db.users.insert_one(user_dict)
    user_dict.pop("password")
    
    return user_dict
