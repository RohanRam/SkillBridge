from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.user import User
from src.models.batch import Batch, BatchInvite, batch_students
from src.schemas.batch import BatchCreate, BatchOut, BatchInviteOut, JoinBatchRequest
from src.core.dependencies import RoleChecker, get_current_user
import uuid
from datetime import datetime, timedelta

router = APIRouter(prefix="/batches", tags=["batches"])

@router.post("", response_model=BatchOut)
def create_batch(
    batch: BatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["trainer", "institution"]))
):
    institution_id = current_user.institution_id if current_user.role == "institution" else current_user.institution_id
    if not institution_id:
        raise HTTPException(status_code=422, detail="User does not belong to an institution")

    new_batch = Batch(name=batch.name, institution_id=institution_id)
    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)

    if current_user.role == "trainer":
        new_batch.trainers.append(current_user)
        db.commit()

    return new_batch

@router.post("/{batch_id}/invite", response_model=BatchInviteOut)
def create_invite(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["trainer"]))
):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    if current_user not in batch.trainers:
        raise HTTPException(status_code=403, detail="Trainer not assigned to this batch")

    token_str = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=7)

    invite = BatchInvite(
        batch_id=batch_id,
        token=token_str,
        created_by=current_user.id,
        expires_at=expires_at
    )
    db.add(invite)
    db.commit()
    db.refresh(invite)

    return {"token": token_str, "expires_at": expires_at}

@router.post("/join")
def join_batch(
    request: JoinBatchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["student"]))
):
    invite = db.query(BatchInvite).filter(BatchInvite.token == request.token).first()
    if not invite:
        raise HTTPException(status_code=404, detail="Invite not found")
    
    if invite.used:
        raise HTTPException(status_code=400, detail="Invite already used")
    
    if invite.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invite expired")

    batch = invite.batch
    if current_user in batch.students:
        raise HTTPException(status_code=400, detail="Already in batch")

    batch.students.append(current_user)
    invite.used = True
    db.commit()

    return {"detail": "Successfully joined batch"}
