# src/services/jwt_service.py

"""
Handles JWT token creation and verification.
"""

from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.config.env import settings

# Use settings for secret key (same as tokens.py)
SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALG
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_MINUTES


def create_access_token(data: dict):
    """
    Create JWT token with expiration time.
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str):
    """
    Decode and verify JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
