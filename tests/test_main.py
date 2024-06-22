import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from todo.database import Base, get_db
from todo.main import app

# Set up a separate database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_todo.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)


# Dependency override to use the testing database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Before tests run
    Base.metadata.create_all(bind=engine)
    yield
    # After tests run
    Base.metadata.drop_all(bind=engine)


def test_create_todo():
    response = client.post("/todos/", data={"title": "Test ToDo"})
    assert response.status_code == 200
    assert "Test ToDo" in response.text


def test_read_todos():
    response = client.get("/todos/")
    assert response.status_code == 200
    assert "Test ToDo" in response.text


def test_toggle_todo():
    response = client.post("/todos/", data={"title": "Another Test ToDo"})
    assert response.status_code == 200

    todo_id = response.text.split('id="todo-')[1].split('"')[0]
    toggle_url = f"/todos/{todo_id}/toggle"

    response = client.put(toggle_url)
    assert response.status_code == 200
    assert "line-through" in response.text


def test_delete_todo():
    response = client.post("/todos/", data={"title": "To Be Deleted"})
    assert response.status_code == 200

    todo_id = response.text.split('id="todo-')[1].split('"')[0]
    delete_url = f"/todos/{todo_id}"

    response = client.delete(delete_url)
    assert response.status_code == 200
    assert response.text == ""
