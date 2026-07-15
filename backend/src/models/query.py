from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from src.config.database import Base


class Query(Base):
    __tablename__ = "queries"
    __table_args__ = {"schema": "software_engineering"}

    query_id = Column(Integer, primary_key=True, index=True)
    query_text = Column(Text, nullable=False)
    normalized_text = Column(Text, nullable=True)

    # source: mobile / whatsapp
    source = Column(String(20), nullable=False, default="mobile")

    # app user OR whatsapp user
    student_user_id = Column(
        Integer,
        ForeignKey("core.users.user_id", ondelete="SET NULL"),
        nullable=True,
    )
    whatsapp_user_id = Column(
        Integer,
        ForeignKey("integration.whatsapp_users.whatsapp_user_id", ondelete="SET NULL"),
        nullable=True,
    )

    detected_language = Column(String(50), nullable=True)
    intent_label = Column(String(100), nullable=True)

    # pending / processing / answered / escalated / assigned / resolved / closed
    status = Column(String(20), nullable=False, default="pending")

    confidence_score = Column(Float, nullable=False, default=0.0)

    matched_kb_id = Column(
        Integer,
        ForeignKey("software_engineering.knowledge_base.kb_id", ondelete="SET NULL"),
        nullable=True,
    )

    matched_attachment_id = Column(
        Integer,
        ForeignKey("software_engineering.attachments.attachment_id", ondelete="SET NULL"),
        nullable=True,
    )

    ai_response = Column(Text, nullable=True)
    escalation_reason = Column(Text, nullable=True)

    assigned_to = Column(
        Integer,
        ForeignKey("core.users.user_id", ondelete="SET NULL"),
        nullable=True,
    )

    # ai / admin / staff
    resolution_type = Column(String(20), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_response_at = Column(DateTime, nullable=True)
    escalated_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)

   
    # Relationships
    
    responses = relationship(
        "Response",
        back_populates="query",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    events = relationship(
        "QueryEvent",
        back_populates="query",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    assignments = relationship(
        "StaffAssignment",
        back_populates="query",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    matched_kb = relationship(
        "KnowledgeBase",
        foreign_keys=[matched_kb_id],
        back_populates="queries",
    )

    matched_attachment = relationship(
        "Attachment",
        foreign_keys=[matched_attachment_id],
        back_populates="matched_queries",
    )

    student_user = relationship(
        "Users",
        foreign_keys=[student_user_id],
        back_populates="submitted_queries",
    )

    assigned_staff = relationship(
        "Users",
        foreign_keys=[assigned_to],
        back_populates="assigned_queries",
    )

    whatsapp_user = relationship(
        "WhatsAppUsers",
        foreign_keys=[whatsapp_user_id],
        back_populates="queries",
    )