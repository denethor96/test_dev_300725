import os
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = os.getenv("SECRET_KEY", "CLAVE")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def create_jwt_token(data: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    to_encode = {**data, "exp": expire}
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)