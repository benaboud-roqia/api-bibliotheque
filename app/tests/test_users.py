import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def test_user():
    return {"username": "testuser", "email": "testuser@example.com", "password": "testpass", "role": "admin"}

def test_register_user(test_user):
    response = client.post("/users/register", json=test_user)
    assert response.status_code == 200 or response.status_code == 400
    if response.status_code == 200:
        data = response.json()
        assert data["role"] == "admin"

def test_login_user(test_user):
    response = client.post("/users/login", data={"username": test_user["username"], "password": test_user["password"]})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    return data["access_token"]

def test_get_profile(test_user):
    login_resp = client.post("/users/login", data={"username": test_user["username"], "password": test_user["password"]})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user["username"] 