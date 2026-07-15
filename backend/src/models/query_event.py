from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class QueryEvent(Base):
    __tablename__ = "query_events"
    __table_args__ = {"schema": "software_engineering"}

    event_id = Column(Integer, primary_key=True, index=True)

    query_id = Column(
        Integer,
        ForeignKey("software_engineering.queries.query_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    event_type = Column(String(50), nullable=False)
    event_message = Column(Text, nullable=True)

    created_by = Column(
        Integer,
        ForeignKey("core.users.user_id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())

   
    # Relationships
    
    query = relationship(
        "Query",
        back_populates="events"
    )

    creator = relationship(
        "Users",
        foreign_keys=[created_by]
    )