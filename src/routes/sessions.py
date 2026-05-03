from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.user import User
from src.models.batch import Batch
from src.models.session import Session as DBSession
from src.models.attendance import Attendance
from src.schemas.session import SessionCreate, SessionOut
from src.schemas.attendance import AttendanceOut
from src.core.dependencies import RoleChecker

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("", response_model=SessionOut)
def create_session(
    session: SessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["trainer"]))
):
    batch = db.query(Batch).filter(Batch.id == session.batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    if current_user not in batch.trainers:
        raise HTTPException(status_code=403, detail="Trainer not assigned to this batch")

    new_session = DBSession(
        batch_id=session.batch_id,
        trainer_id=current_user.id,
        title=session.title,
        date=session.date,
        start_time=session.start_time,
        end_time=session.end_time
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session

@router.get("/{session_id}/attendance", response_model=list[AttendanceOut])
def get_session_attendance(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["trainer"]))
):
    session = db.query(DBSession).filter(DBSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.trainer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this session's attendance")

    attendances = db.query(Attendance).filter(Attendance.session_id == session_id).all()
    return attendances
