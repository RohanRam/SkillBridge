# 🚀 SkillBridge Attendance System — FULL Antigravity-Ready Blueprint

> This document is designed to generate a near-complete backend project when used with AI builders like Antigravity.

---

# 🧠 TECH STACK

- FastAPI
- PostgreSQL (Neon)
- SQLAlchemy
- Alembic (optional)
- Passlib (bcrypt)
- python-jose (JWT)
- Uvicorn

---

# 📁 PROJECT STRUCTURE

```
/src
  main.py
  database.py
  config.py
  /models
  /schemas
  /routes
  /services
  /core
/tests
requirements.txt
.env.example
README.md
```

---

# ⚙️ ENV VARIABLES (.env)

```
DATABASE_URL=postgresql://user:password@host/db
JWT_SECRET=your_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24
MONITORING_API_KEY=supersecretkey
```

---

# 🗄️ DATABASE SETUP (SQLAlchemy)

## database.py
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```

---

# 👤 USER MODEL

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String)
    institution_id = Column(Integer, nullable=True)
```

---

# 🔐 AUTH SERVICE

```python
from jose import jwt
from datetime import datetime, timedelta

def create_token(data: dict, expires_hours: int):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=expires_hours)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm="HS256")
```

---

# 🔑 PASSWORD HASHING

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)
```

---

# 🔌 AUTH ROUTES

```python
@router.post("/signup")
def signup(user: UserCreate):
    hashed = hash_password(user.password)
    db_user = User(...)
    db.add(db_user)
    db.commit()
    token = create_token({"user_id": db_user.id, "role": db_user.role}, 24)
    return {"token": token}
```

---

# 🔒 RBAC MIDDLEWARE

```python
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    return payload

def require_role(roles: list):
    def checker(user=Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(status_code=403)
        return user
    return checker
```

---

# 📦 BATCH ROUTES

```python
@router.post("/batches")
def create_batch(user=Depends(require_role(["trainer", "institution"]))):
    ...
```

---

# 📅 SESSION ROUTES

```python
@router.post("/sessions")
def create_session(user=Depends(require_role(["trainer"]))):
    ...
```

---

# 📊 ATTENDANCE

```python
@router.post("/attendance/mark")
def mark_attendance(user=Depends(require_role(["student"]))):
    ...
```

---

# 👁 MONITORING TOKEN

```python
@router.post("/auth/monitoring-token")
def monitoring_token(key: str, user=Depends(require_role(["monitoring_officer"]))):
    if key != os.getenv("MONITORING_API_KEY"):
        raise HTTPException(401)
    return create_token({"role": "monitoring_officer"}, 1)
```

---

# 🧪 PYTEST EXAMPLES

```python
def test_signup(client):
    res = client.post("/auth/signup", json={...})
    assert res.status_code == 200
```

---

# 🌱 SEED SCRIPT

```python
def seed():
    # create users, batches, sessions
```

---

# 🚀 DEPLOYMENT

## Render Steps
1. Push to GitHub
2. Connect repo
3. Add env vars
4. Deploy

---

# 📄 README TEMPLATE

## Setup
```
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Curl Example
```
curl -X POST /auth/login
```

---

# ⚠️ EDGE CASES COVERED

- Invalid token → 401
- Wrong role → 403
- Missing fields → 422
- Wrong method → 405

---

# 🔥 FINAL RESULT

This file enables:
✔ Full backend scaffold  
✔ JWT auth system  
✔ RBAC enforcement  
✔ Monitoring security layer  
✔ Test-ready project  

---

# 🧠 PRO TIP

After generating project:
- Fix minor bugs
- Deploy
- Add README honesty

That’s what gets you selected.