from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.user import User
from src.schemas.user import UserCreate, Token, MonitoringTokenRequest
from src.core.security import hash_password, verify_password, create_access_token, create_monitoring_token
from src.core.dependencies import get_current_user, RoleChecker
from src.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if user.role not in ["student", "trainer", "institution", "programme_manager", "monitoring_officer"]:
        raise HTTPException(status_code=422, detail="Invalid role")

    hashed_pw = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role,
        institution_id=user.institution_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"user_id": new_user.id, "role": new_user.role})
    return {"access_token": access_token, "token_type": "bearer"}

from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"user_id": user.id, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/monitoring-token", response_model=Token)
def get_monitoring_token(
    request: MonitoringTokenRequest,
    current_user: User = Depends(RoleChecker(["monitoring_officer"]))
):
    if request.key != settings.MONITORING_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid monitoring API key")
    
    monitoring_token = create_monitoring_token(data={"user_id": current_user.id, "role": current_user.role})
    return {"access_token": monitoring_token, "token_type": "bearer"}
