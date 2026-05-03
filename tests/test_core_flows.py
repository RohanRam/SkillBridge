from src.models.batch import Batch
from src.core.security import create_access_token

def test_trainer_creates_session(client, db_session, test_trainer):
    # Setup batch
    b = Batch(name="Test Batch", institution_id=1)
    db_session.add(b)
    db_session.commit()
    b.trainers.append(test_trainer)
    db_session.commit()

    token = create_access_token({"user_id": test_trainer.id, "role": test_trainer.role})
    
    res = client.post("/sessions", json={
        "batch_id": b.id,
        "title": "First Session",
        "date": "2024-01-01",
        "start_time": "10:00",
        "end_time": "12:00"
    }, headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 200
    assert res.json()["title"] == "First Session"

def test_student_marks_attendance(client, db_session, test_student, test_trainer):
    # Setup
    b = Batch(name="Test Batch", institution_id=1)
    db_session.add(b)
    db_session.commit()
    b.students.append(test_student)
    db_session.commit()

    from src.models.session import Session as DBSession
    from datetime import date, time
    s = DBSession(batch_id=b.id, trainer_id=test_trainer.id, title="Test", date=date.today(), start_time=time(10,0), end_time=time(12,0))
    db_session.add(s)
    db_session.commit()

    token = create_access_token({"user_id": test_student.id, "role": test_student.role})
    
    res = client.post("/attendance/mark", json={
        "session_id": s.id,
        "status": "present"
    }, headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 200
    assert res.json()["status"] == "present"
