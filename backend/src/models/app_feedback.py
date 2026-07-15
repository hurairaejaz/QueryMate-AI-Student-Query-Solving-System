from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.models.base import Base


class AppFeedback(Base):
    __tablename__ = "app_feedback"
    __table_args__ = {"schema": "core"}

    feedback_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("core.users.user_id", ondelete="SET NULL"))
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())