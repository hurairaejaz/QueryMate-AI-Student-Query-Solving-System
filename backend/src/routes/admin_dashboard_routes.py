from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.config.database import get_db
from src.models.query import Query
from src.models.response import Response

router = APIRouter(prefix="/admin/dashboard", tags=["Admin Dashboard"])


@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_queries = db.query(Query).count()

    escalated_queries = (
        db.query(Query)
        .filter(Query.status == "escalated")
        .count()
    )

    responded_queries = (
        db.query(Query)
        .filter(Query.status.in_(["answered", "resolved", "closed"]))
        .count()
    )

    latest_escalated = (
        db.query(Query)
        .filter(Query.status == "escalated")
        .order_by(Query.created_at.desc())
        .limit(10)
        .all()
    )

    return {
        "total_queries": total_queries,
        "escalated_queries": escalated_queries,
        "responded_queries": responded_queries,
        "latest_escalated": [
            {
                "query_id": q.query_id,
                "query_text": q.query_text,
                "source": q.source,
                "status": q.status,
                "created_at": q.created_at,
            }
            for q in latest_escalated
        ],
    }