from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.services.dependencies import get_current_user_either
from src.models.app_feedback import AppFeedback
from src.schemas.app_feedback import AppFeedbackCreate

router = APIRouter(prefix="/app/feedback", tags=["App Feedback"])


@router.post("/")
def submit_feedback(
    payload: AppFeedbackCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_either),
):
    feedback = AppFeedback(
        user_id=current_user.get("user_id"),
        rating=payload.rating,
        comment=payload.comment,
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return {
        "message": "Feedback submitted successfully",
        "feedback_id": feedback.feedback_id,
    }


@router.get("/admin")
def list_feedback(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_either),
):
    items = (
        db.query(AppFeedback)
        .order_by(AppFeedback.created_at.desc())
        .all()
    )

    return {
        "items": [
            {
                "feedback_id": f.feedback_id,
                "user_id": f.user_id,
                "rating": f.rating,
                "comment": f.comment,
                "created_at": f.created_at,
            }
            for f in items
        ],
        "total": len(items),
    }