def test_no_token_returns_401(client):
    res = client.post("/sessions", json={
        "batch_id": 1,
        "title": "Hack",
        "date": "2024-01-01",
        "start_time": "10:00",
        "end_time": "12:00"
    })
    assert res.status_code == 401

def test_monitoring_post_returns_405(client):
    # Even without token, fastapi router checks method first or throws 405
    res = client.post("/monitoring/attendance")
    assert res.status_code == 405
