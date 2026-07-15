# CHANGE: Profile update route for mobile app user

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.user import Users
from src.schemas.profile_schema import ProfileUpdateRequest
from src.services.dependencies import get_current_user_either

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.patch("/update")
def update_profile(
    payload: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_either),
):
    user_id = current_user.get("user_id") or current_user.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user token")

    user = db.query(Users).filter(Users.user_id == int(user_id)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.full_name = payload.full_name
    user.phone = payload.phone

    db.commit()
    db.refresh(user)

    return {
        "message": "Profile updated successfully",
        "user": {
            "user_id": user.user_id,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
        },
    }