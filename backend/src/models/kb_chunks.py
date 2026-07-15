from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class KBChunk(Base):
    __tablename__ = "kb_chunks"
    __table_args__ = {"schema": "software_engineering"}

    chunk_id = Column(Integer, primary_key=True, index=True)

    kb_id = Column(
        Integer,
        ForeignKey("software_engineering.knowledge_base.kb_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    attachment_id = Column(
        Integer,
        ForeignKey("software_engineering.attachments.attachment_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    chunk_index = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

   
    # Relationships
   
    kb_entry = relationship(
        "KnowledgeBase",
        back_populates="chunks"
    )

    attachment = relationship(
        "Attachment",
        back_populates="chunks"
    )