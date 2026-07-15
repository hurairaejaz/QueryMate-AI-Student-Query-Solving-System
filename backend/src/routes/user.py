from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from src.models.notification import Notification
from src.models.query import Query
from src.models.user import Users

from src.config.database import get_db
from src.services.dependencies import get_current_user_either

router = APIRouter(prefix="/user")

@router.delete("/delete-account")
def delete_account(db: Session = Depends(get_db), current_user=Depends(get_current_user_either)):
    try:
        user_id = int(current_user["id"])

        user = db.query(Users).filter(Users.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        #  delete child records
        db.query(Query).filter(Query.user_id == user_id).delete()
        db.query(Notification).filter(Notification.user_id == user_id).delete()
        # db.query(History).filter(History.user_id == user_id).delete()

        #  delete user
        db.delete(user)
        db.commit()

        return {"message": "Account deleted successfully"}

    except Exception as e:
        db.rollback()
        print("DELETE ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))