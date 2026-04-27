from datetime import datetime, timedelta
from jose import jwt
import os


def create_access_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=8)
    }

    return jwt.encode(
        payload,
        os.getenv("JWT_SECRET"),
        algorithm="HS256"
    )