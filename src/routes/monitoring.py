from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.attendance import Attendance
from src.core.dependencies import get_monitoring_user

router = APIRouter(prefix="/monitoring", tags=["monitoring"])

@router.get("/attendance")
def get_all_attendance(
    db: Session = Depends(get_db),
    monitoring_token_payload: dict = Depends(get_monitoring_user)
):
    # This route uses the get_monitoring_user dependency which validates the scoped short-lived token
    # It also inherently rejects non-GET requests with a 405 Method Not Allowed due to the @router.get decorator.
    attendances = db.query(Attendance).all()
    return [{"id": a.id, "session_id": a.session_id, "student_id": a.student_id, "status": a.status, "marked_at": a.marked_at} for a in attendances]
