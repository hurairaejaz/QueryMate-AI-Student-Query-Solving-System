from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class AuthToken(Base):
    __tablename__ = "auth_tokens"
    __table_args__ = {"schema": "core"}

    token_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("core.users.user_id", ondelete="CASCADE"), nullable=False)

    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
