import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from todo.database import Base, get_db
from todo.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_todo.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    yield
    os.remove("./test_todo.db")


def test_create_todo():
    response = client.post("/todos/", data={"title": "Test ToDo"})
    assert response.status_code == 200
    assert "Test ToDo" in response.text


def test_read_todos():
    response = client.get("/todos/")
    assert response.status_code == 200
    assert "Test ToDo" in response.text


def test_toggle_todo():
    response = client.post("/todos/", data={"title": "Toggle ToDo"})
    assert response.status_code == 200
    todo_id = int(response.text.split('id="todo-')[1].split('"')[0])
    response = client.put(f"/todos/{todo_id}/toggle")
    assert response.status_code == 200


def test_delete_todo():
    response = client.post("/todos/", data={"title": "Delete ToDo"})
    assert response.status_code == 200
    todo_id = int(response.text.split('id="todo-')[1].split('"')[0])
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.text == ""
