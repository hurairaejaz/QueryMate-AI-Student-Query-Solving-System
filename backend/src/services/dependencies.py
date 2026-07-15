from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.utils.tokens import decode_token

security = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="No authorization header provided")

    token = credentials.credentials
    try:
        payload = decode_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload


def get_current_user_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="No access token in cookies")

    try:
        payload = decode_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload


def get_current_user_either(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = None

    #  Try cookie first
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        token = cookie_token

    #  Fallback to Authorization header
    elif credentials and credentials.credentials:
        token = credentials.credentials

    if not token:
        raise HTTPException(status_code=401, detail="No token provided")

    try:
        payload = decode_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload


def admin_only(user=Depends(get_current_user_either)):
    if user.get("role") not in ("admin", "superadmin"):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user