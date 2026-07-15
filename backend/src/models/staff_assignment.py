from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class StaffAssignment(Base):
    __tablename__ = "staff_assignments"
    __table_args__ = {"schema": "software_engineering"}

    assignment_id = Column(Integer, primary_key=True, index=True)

    query_id = Column(
        Integer,
        ForeignKey("software_engineering.queries.query_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    assigned_to = Column(
        Integer,
        ForeignKey("core.users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    assigned_by = Column(
        Integer,
        ForeignKey("core.users.user_id", ondelete="SET NULL"),
        nullable=True,
    )

    notes = Column(Text, nullable=True)

    # assigned / in_progress / completed / cancelled
    status = Column(String(20), nullable=False, default="assigned")

    assigned_at = Column(DateTime(timezone=True), server_default=func.now())

    
    # Relationships
    
    query = relationship(
        "Query",
        back_populates="assignments"
    )

    assigned_staff = relationship(
        "Users",
        foreign_keys=[assigned_to]
    )

    assigned_by_user = relationship(
        "Users",
        foreign_keys=[assigned_by]
    )
    