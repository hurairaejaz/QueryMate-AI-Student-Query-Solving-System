from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from src.config.database import Base


class Response(Base):
    __tablename__ = "responses"
    __table_args__ = {"schema": "software_engineering"}

    response_id = Column(Integer, primary_key=True, index=True)

    query_id = Column(
        Integer,
        ForeignKey("software_engineering.queries.query_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    response_text = Column(Text, nullable=False)

    # ai / admin / staff
    response_type = Column(String(20), nullable=False, default="ai")

    # nullable for AI, filled for admin/staff
    responder_id = Column(
        Integer,
        ForeignKey("core.users.user_id", ondelete="SET NULL"),
        nullable=True,
    )

    confidence_score = Column(Float, nullable=False, default=0.0)
    tone_used = Column(String(50), nullable=True)
    source_evidence = Column(Text, nullable=True)

    attachment_id = Column(
        Integer,
        ForeignKey("software_engineering.attachments.attachment_id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    
    # Relationships
    
    query = relationship(
        "Query",
        back_populates="responses",
    )

    responder = relationship(
        "Users",
        foreign_keys=[responder_id],
    )

    attachment = relationship(
        "Attachment",
        foreign_keys=[attachment_id],
        back_populates="responses",
    )