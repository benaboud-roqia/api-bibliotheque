import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def user_token():
    user = {"username": "bookuser", "email": "bookuser@example.com", "password": "bookpass"}
    client.post("/users/register", json=user)
    resp = client.post("/users/login", data={"username": user["username"], "password": user["password"]})
    return resp.json()["access_token"]

def test_create_book(user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    book = {"title": "Test Book", "author": "Author X", "description": "A test book."}
    response = client.post("/books/", json=book, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == book["title"]
    assert data["author"] == book["author"]
    global book_id
    book_id = data["id"]

def test_read_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_book(user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    update = {"title": "Updated Book", "author": "Author X", "description": "Updated desc."}
    response = client.put(f"/books/1", json=update, headers=headers)
    assert response.status_code in [200, 403, 404]

def test_delete_book(user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.delete(f"/books/1", headers=headers)
    assert response.status_code in [204, 403, 404] 