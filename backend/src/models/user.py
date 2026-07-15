from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from .base import Base
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "core", "extend_existing": True}
 
    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="student")
    is_active = Column(Boolean, default=True)
    otp_code = Column(String, nullable=True)
    otp_expiry = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    # roll_number = Column(String, unique=True, nullable=True)
    # is_email_verified = Column(Boolean, default=False, nullable=False)
    is_deleted = Column(Boolean, default=False)
    # queries = relationship("Query", back_populates="student")
    submitted_queries = relationship(
        "Query",
        foreign_keys="Query.student_user_id",
        back_populates="student_user",
    )

    assigned_queries = relationship(
        "Query",
        foreign_keys="Query.assigned_to",
        back_populates="assigned_staff",
    )
    
    
class AuthToken(Base):
    __tablename__ = "auth_tokens"
    __table_args__ = {"schema": "core", "extend_existing": True}

    token_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("core.users.user_id"), nullable=False)
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text)
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
 

class Departments(Base):
    __tablename__ = "departments"
    __table_args__ = {"schema": "core", "extend_existing": True}

    department_id = Column(Integer, primary_key=True, index=True)
    department_key = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(200), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Feedback(Base):
    __tablename__ = "feedback"
    __table_args__ = {"schema": "core", "extend_existing": True}

    feedback_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("core.users.user_id"), nullable=True)
    rating = Column(Integer)
    comments = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ActivityLogs(Base):
    __tablename__ = "activity_logs"
    __table_args__ = {"schema": "core", "extend_existing": True}

    log_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("core.users.user_id"), nullable=True)
    action_type = Column(String(100))
    details = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
