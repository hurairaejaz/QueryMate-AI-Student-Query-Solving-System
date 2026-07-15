from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from src.models.base import Base

class PasswordResetOTP(Base):
    __tablename__ = "password_reset_otps"
    __table_args__ = {"schema": "core"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("core.users.user_id"), nullable=False)
    identifier = Column(String, nullable=False)
    otp_code = Column(String(6), nullable=False)
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)