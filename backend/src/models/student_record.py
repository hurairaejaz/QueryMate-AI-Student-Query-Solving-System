from sqlalchemy import Column, Integer, String
from src.config.database import Base

class StudentRecord(Base):
    __tablename__ = "student_records"

    id = Column(Integer, primary_key=True)
    roll_number = Column(String, nullable=True)
    name = Column(String)