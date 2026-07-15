from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base


class WhatsAppMessages(Base):
    __tablename__ = "whatsapp_messages"
    __table_args__ = {"schema": "integration", "extend_existing": True}

    message_id = Column(Integer, primary_key=True, index=True)

    whatsapp_user_id = Column(
        Integer,
        ForeignKey("integration.whatsapp_users.whatsapp_user_id", ondelete="CASCADE"),
        nullable=False,
    )

    query_id = Column(
        Integer,
        ForeignKey("software_engineering.queries.query_id"),
        nullable=True,
    )

    direction = Column(String(10), nullable=False)  # inbound / outbound

    
    message_type = Column(String(30), default="text")

    message_text = Column(Text, nullable=True)

    
    media_url = Column(Text, nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    meta_message_id = Column(String(255), unique=True, nullable=True, index=True)

    whatsapp_user = relationship("WhatsAppUsers", back_populates="messages")
class ExternalSystems(Base):
    __tablename__ = "external_systems"
    __table_args__ = {"schema": "integration", "extend_existing": True}

    system_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    api_key = Column(Text, nullable=True)
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
