from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.services.auth_services import register_admin, login_admin

def admin_register_controller(db: Session, full_name: str, email: str, password: str):
    try:
        user = register_admin(db, full_name, email, password)
        return {"message": "Admin registered successfully.", "user_id": user.user_id, "email": user.email}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

def admin_login_controller(db: Session, email: str, password: str):
    try:
        return login_admin(db, email, password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))