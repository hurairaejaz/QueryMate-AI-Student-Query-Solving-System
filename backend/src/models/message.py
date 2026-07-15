from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from src.config.database import Base


# CHAT MESSAGES TABLE

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, index=True)

    query_id = Column(Integer, ForeignKey("queries.query_id"))
    sender_id = Column(Integer, ForeignKey("users.user_id"))

    message_text = Column(Text)
    attachment_id = Column(Integer, ForeignKey("attachments.attachment_id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())