from fastapi import FastAPI
from src.database import engine, Base
from src.routes import auth, batches, sessions, attendance, reports, monitoring

# Initialize database
Base.metadata.create_all(bind=engine)

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
