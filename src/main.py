from fastapi import FastAPI
from src.database import engine, Base
from src.routes import auth, batches, sessions, attendance, reports, monitoring

import sys
import traceback

# Initialize database
try:
    Base.metadata.create_all(bind=engine)
    print("Database connected and initialized successfully!")
except Exception as e:
    print("\n" + "="*50)
    print("🚨 DATABASE CONNECTION OR INITIALIZATION FAILED 🚨")
    print("="*50)
    traceback.print_exc()
    print("="*50 + "\n")
    sys.exit(1)
app = FastAPI(title="SkillBridge Attendance Management API")

app.include_router(auth.router)
app.include_router(batches.router)
app.include_router(sessions.router)
app.include_router(attendance.router)
app.include_router(reports.router)
app.include_router(monitoring.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the SkillBridge Attendance API"}
