from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"
    __table_args__ = {"schema": "software_engineering"}

    kb_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(250), nullable=False)
    content = Column(Text, nullable=False)

    category_id = Column(
        Integer,
        ForeignKey("software_engineering.kb_categories.category_id"),
        nullable=True
    )

    department_key = Column(String(100), nullable=False)

    created_by = Column(
        Integer,
        ForeignKey("core.users.user_id"),
        nullable=True
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    
    # Relationships
    
    queries = relationship(
        "Query",
        back_populates="matched_kb"
    )

    attachments = relationship(
        "Attachment",
        back_populates="kb_entry",
        cascade="all, delete-orphan"
    )

    chunks = relationship(
        "KBChunk",
        back_populates="kb_entry",
        cascade="all, delete-orphan"
    )

    category = relationship(
        "KbCategory",
        back_populates="kb_entries"
    )


class KbCategory(Base):
    __tablename__ = "kb_categories"
    __table_args__ = {"schema": "software_engineering"}

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(255), nullable=False)

    kb_entries = relationship(
        "KnowledgeBase",
        back_populates="category"
    )