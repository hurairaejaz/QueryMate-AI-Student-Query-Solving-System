from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from src.config.env import settings
from src.models.user import Users
def _now():
    return datetime.now(timezone.utc)

def create_access_token(user_id: int, role: str):
    exp = _now() + timedelta(minutes=settings.ACCESS_TOKEN_MINUTES)
    payload = {
        "user_id": user_id,
        "role": role,
        "type": "access",
        "exp": exp,
    }

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    return token, exp

def create_refresh_token(user_id: int, role: str):
    exp = _now() + timedelta(days=settings.REFRESH_TOKEN_DAYS)
    payload = {
        "user_id": user_id,
        "role": role,
        "type": "refresh",
        "exp": exp,
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    return token, exp

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except JWTError:
        raise ValueError("Invalid token")

