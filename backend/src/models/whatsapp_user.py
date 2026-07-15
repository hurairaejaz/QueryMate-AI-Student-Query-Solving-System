from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base


class WhatsAppUsers(Base):
    __tablename__ = "whatsapp_users"
    __table_args__ = {"schema": "integration", "extend_existing": True}

    whatsapp_user_id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=True)
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), nullable=True)

    messages = relationship(
        "WhatsAppMessages",
        back_populates="whatsapp_user",
        cascade="all, delete-orphan",
    )

    queries = relationship(
        "Query",
        foreign_keys="Query.whatsapp_user_id",
        back_populates="whatsapp_user",
    )