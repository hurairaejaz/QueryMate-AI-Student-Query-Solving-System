from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.services.dependencies import get_current_user_either
from src.models.notification import Notification

router = APIRouter(prefix="/app/notifications", tags=["Notifications"])


@router.get("/")
def list_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_either),
):
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.get("user_id"))
        .order_by(Notification.created_at.desc())
        .all()
    )

    items = []
    for n in notifications:
        items.append({
            "notification_id": n.notification_id,
            "user_id": n.user_id,
            "query_id": n.query_id,
            "title": n.title,
            "message": n.message,
            "type": n.type,
            "is_read": n.is_read,
            "created_at": n.created_at,
        })

    return {"items": items, "total": len(items)}


@router.post("/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_either),
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.notification_id == notification_id,
            Notification.user_id == current_user.get("user_id"),
        )
        .first()
    )

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.is_read = True
    db.commit()
    db.refresh(notification)

    return {
        "message": "Notification marked as read.",
        "notification_id": notification.notification_id,
        "is_read": notification.is_read,
    }