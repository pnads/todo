from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from todo.crud import create_todo, delete_todo, get_todos, toggle_todo
from todo.database import get_db

router = APIRouter()


def todo_to_html(todo):
    return f"""
    <li id="todo-{todo.id}" class="flex items-center justify-between bg-white p-4 rounded-md shadow">
        <span class="{'line-through text-gray-500' if todo.completed else 'text-gray-900'}">{todo.title}</span>
        <div>
            <button hx-put="/todos/{todo.id}/toggle" hx-target="#todo-{todo.id}" hx-swap="outerHTML"
                class="px-3 py-1 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 mr-2">
                Toggle
            </button>
            <button hx-delete="/todos/{todo.id}" hx-target="#todo-{todo.id}" hx-swap="outerHTML"
                class="px-3 py-1 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50">
                Delete
            </button>
        </div>
    </li>
    """


@router.post("/todos/")
async def create_todo_route(title: str = Form(...), db: Session = Depends(get_db)):
    db_todo = create_todo(db, title)
    return HTMLResponse(todo_to_html(db_todo))


@router.get("/todos/")
async def read_todos_route(db: Session = Depends(get_db)):
    todos = get_todos(db)
    return HTMLResponse("".join(todo_to_html(todo) for todo in todos))


@router.put("/todos/{todo_id}/toggle")
async def toggle_todo_route(todo_id: int, db: Session = Depends(get_db)):
    db_todo = toggle_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return HTMLResponse(todo_to_html(db_todo))


@router.delete("/todos/{todo_id}")
async def delete_todo_route(todo_id: int, db: Session = Depends(get_db)):
    if not delete_todo(db, todo_id):
        raise HTTPException(status_code=404, detail="ToDo not found")
    return HTMLResponse("")
