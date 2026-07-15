from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.models.user import Users

router = APIRouter(prefix="/admin/profile", tags=["Admin Profile"])


@router.get("/by-email")
def get_admin_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "full_name": user.full_name
    }