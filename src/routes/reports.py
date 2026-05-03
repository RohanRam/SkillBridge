from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.user import User
from src.models.batch import Batch
from src.models.session import Session as DBSession
from src.models.attendance import Attendance
from src.core.dependencies import RoleChecker

router = APIRouter(tags=["reports"])

@router.get("/batches/{batch_id}/summary")
def get_batch_summary(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["institution"]))
):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    if batch.institution_id != current_user.institution_id:
        raise HTTPException(status_code=403, detail="Batch not under your institution")

    sessions = db.query(DBSession).filter(DBSession.batch_id == batch_id).all()
    session_ids = [s.id for s in sessions]
    
    attendances = db.query(Attendance).filter(Attendance.session_id.in_(session_ids)).all()
    
    return {
        "batch_id": batch_id,
        "total_sessions": len(sessions),
        "total_attendances": len(attendances)
    }

@router.get("/institutions/{institution_id}/summary")
def get_institution_summary(
    institution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["programme_manager"]))
):
    batches = db.query(Batch).filter(Batch.institution_id == institution_id).all()
    batch_ids = [b.id for b in batches]
    
    sessions = db.query(DBSession).filter(DBSession.batch_id.in_(batch_ids)).all()
    session_ids = [s.id for s in sessions]
    
    attendances = db.query(Attendance).filter(Attendance.session_id.in_(session_ids)).all()

    return {
        "institution_id": institution_id,
        "total_batches": len(batches),
        "total_sessions": len(sessions),
        "total_attendances": len(attendances)
    }

@router.get("/programme/summary")
def get_programme_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["programme_manager"]))
):
    total_institutions = db.query(User).filter(User.role == "institution").count()
    total_batches = db.query(Batch).count()
    total_sessions = db.query(DBSession).count()
    total_attendances = db.query(Attendance).count()

    return {
        "total_institutions": total_institutions,
        "total_batches": total_batches,
        "total_sessions": total_sessions,
        "total_attendances": total_attendances
    }
