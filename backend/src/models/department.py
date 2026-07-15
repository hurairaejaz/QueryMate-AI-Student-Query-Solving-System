from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from src.models.base import Base


class Department(Base):
    __tablename__ = "departments"
    __table_args__ = {"schema": "core", "extend_existing": True}

    department_id = Column(Integer, primary_key=True, index=True)
    department_key = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(200), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())