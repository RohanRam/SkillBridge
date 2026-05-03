from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class AttendanceMark(BaseModel):
    session_id: int
    status: Literal['present', 'absent', 'late']

class AttendanceOut(BaseModel):
    id: int
    session_id: int
    student_id: int
    status: str
    marked_at: datetime

    class Config:
        from_attributes = True
