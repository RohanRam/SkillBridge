def test_signup_and_login(client):
    # 1. Successful student signup
    res = client.post("/auth/signup", json={
        "name": "New Student",
        "email": "new@student.com",
        "password": "password123",
        "role": "student"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()

    # 2. Login
    res2 = client.post("/auth/login", data={
        "username": "new@student.com",
        "password": "password123"
    })
    assert res2.status_code == 200
    assert "access_token" in res2.json()
