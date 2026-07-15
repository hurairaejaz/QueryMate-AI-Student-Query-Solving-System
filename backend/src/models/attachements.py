from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from src.config.database import Base


class Attachment(Base):
    __tablename__ = "attachments"
    __table_args__ = {"schema": "software_engineering"}

    attachment_id = Column(Integer, primary_key=True, index=True)

    kb_id = Column(
        Integer,
        ForeignKey("software_engineering.knowledge_base.kb_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    file_name = Column(String(255), nullable=False)
    file_url = Column(Text, nullable=True)
    mime_type = Column(String(100), nullable=True)
    file_type = Column(String(50), nullable=True)   # pdf / docx / txt / image
    drive_file_id = Column(String(255), nullable=True)

    # local / drive / supabase
    storage_type = Column(String(20), nullable=False, default="local")

    # extracted text from document for chunking/retrieval
    extracted_text = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # -----------------------------
    # Relationships
    # -----------------------------
    kb_entry = relationship(
        "KnowledgeBase",
        back_populates="attachments",
    )

    chunks = relationship(
        "KBChunk",
        back_populates="attachment",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    responses = relationship(
       "Response",
       foreign_keys="Response.attachment_id",
       back_populates="attachment",
   )

    matched_queries = relationship(
        "Query",
        foreign_keys="Query.matched_attachment_id",
        back_populates="matched_attachment",
    )