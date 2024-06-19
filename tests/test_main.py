from fastapi.testclient import TestClient

from todo.main import app

client = TestClient(app)


def test_create_todo():
    response = client.post(
        "/todos/",
        json={
            "title": "Test Todo",
            "description": "This is a test todo",
            "completed": False,
        },
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Todo"
    assert response.json()["description"] == "This is a test todo"


def test_read_todos():
    response = client.get("/todos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
