from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schema
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

db = get_db()


@app.post("/todos/", response_model=schema.Todo)
def create_todo(todo: schema.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo_item(db=db, todo=todo)


@app.get("/todos/", response_model=list[schema.Todo])
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos


@app.get("/todos/{todo_id}", response_model=schema.Todo)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.delete("/todos/{todo_id}", response_model=schema.Todo)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return crud.delete_todo_item(db=db, todo_id=todo_id)
