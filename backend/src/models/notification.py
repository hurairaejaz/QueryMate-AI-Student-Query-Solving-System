from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = {"schema": "core"}

    notification_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("core.users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    query_id = Column(
        Integer,
        ForeignKey("software_engineering.queries.query_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), nullable=False, default="query_answered")

    is_read = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("Users", foreign_keys=[user_id])
    query = relationship("Query", foreign_keys=[query_id])