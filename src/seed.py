from sqlalchemy.orm import Session
from src.database import SessionLocal, engine, Base
from src.models.user import User
from src.models.batch import Batch
from src.models.session import Session as DBSession
from src.models.attendance import Attendance
from src.core.security import hash_password
from datetime import date, time, timedelta

def seed_data():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    # Check if already seeded
    if db.query(User).count() > 0:
        print("Database already seeded.")
        db.close()
        return

    print("Seeding database...")
    default_pw = hash_password("password123")

    # 1 Programme Manager
    pm = User(name="Program Manager", email="pm@test.com", hashed_password=default_pw, role="programme_manager")
    # 1 Monitoring Officer
    mo = User(name="Monitoring Officer", email="mo@test.com", hashed_password=default_pw, role="monitoring_officer")
    db.add_all([pm, mo])
    db.commit()

    # 2 Institutions
    inst1 = User(name="Institution One", email="inst1@test.com", hashed_password=default_pw, role="institution")
    inst2 = User(name="Institution Two", email="inst2@test.com", hashed_password=default_pw, role="institution")
    db.add_all([inst1, inst2])
    db.commit()
    db.refresh(inst1)
    db.refresh(inst2)

    # 4 Trainers
    trainers = []
    for i in range(1, 5):
        t = User(name=f"Trainer {i}", email=f"trainer{i}@test.com", hashed_password=default_pw, role="trainer", institution_id=inst1.id if i <= 2 else inst2.id)
        db.add(t)
        trainers.append(t)
    db.commit()

    # 15 Students
    students = []
    for i in range(1, 16):
        s = User(name=f"Student {i}", email=f"student{i}@test.com", hashed_password=default_pw, role="student")
        db.add(s)
        students.append(s)
    db.commit()

    # 3 Batches
    b1 = Batch(name="Batch Alpha", institution_id=inst1.id)
    b2 = Batch(name="Batch Beta", institution_id=inst1.id)
    b3 = Batch(name="Batch Gamma", institution_id=inst2.id)
    db.add_all([b1, b2, b3])
    db.commit()

    # Assign trainers
    b1.trainers.append(trainers[0])
    b2.trainers.append(trainers[1])
    b3.trainers.extend([trainers[2], trainers[3]])
    
    # Assign students (5 per batch)
    b1.students.extend(students[0:5])
    b2.students.extend(students[5:10])
    b3.students.extend(students[10:15])
    db.commit()

    # 8 Sessions
    sessions = []
    for i in range(1, 9):
        batch = b1 if i <= 3 else (b2 if i <= 5 else b3)
        trainer = batch.trainers[0]
        s = DBSession(
            batch_id=batch.id,
            trainer_id=trainer.id,
            title=f"Session {i}",
            date=date.today() - timedelta(days=i),
            start_time=time(10, 0),
            end_time=time(12, 0)
        )
        db.add(s)
        sessions.append(s)
    db.commit()

    # Attendance
    import random
    for session in sessions:
        batch = db.query(Batch).get(session.batch_id)
        for student in batch.students:
            a = Attendance(
                session_id=session.id,
                student_id=student.id,
                status=random.choice(["present", "present", "late", "absent"])
            )
            db.add(a)
    db.commit()
    
    print("Seeding complete.")
    db.close()

if __name__ == "__main__":
    seed_data()
