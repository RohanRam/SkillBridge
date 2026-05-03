from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.user import User
from src.models.session import Session as DBSession
from src.models.attendance import Attendance
from src.schemas.attendance import AttendanceMark, AttendanceOut
from src.core.dependencies import RoleChecker

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.post("/mark", response_model=AttendanceOut)
def mark_attendance(
    attendance: AttendanceMark,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["student"]))
):
    session = db.query(DBSession).filter(DBSession.id == attendance.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    batch = session.batch_id
    from src.models.batch import Batch
    batch_obj = db.query(Batch).filter(Batch.id == batch).first()
    if current_user not in batch_obj.students:
        raise HTTPException(status_code=403, detail="Student not enrolled in this session's batch")

    # Check if already marked
    existing_attendance = db.query(Attendance).filter(
        Attendance.session_id == attendance.session_id,
        Attendance.student_id == current_user.id
    ).first()

    if existing_attendance:
        existing_attendance.status = attendance.status
        db.commit()
        db.refresh(existing_attendance)
        return existing_attendance

    new_attendance = Attendance(
        session_id=attendance.session_id,
        student_id=current_user.id,
        status=attendance.status
    )
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance
