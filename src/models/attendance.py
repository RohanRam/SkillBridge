from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from src.database import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False) # present, absent, late
    marked_at = Column(DateTime, default=datetime.utcnow)
