import datetime

from sqlalchemy.orm import Session

from todo.models import ToDo
from todo.schemas import ToDoCreate


def get_todos(db: Session):
    return db.query(ToDo).all()


def create_todo(db: Session, todo: ToDoCreate):
    db_todo = ToDo(
        title=todo.title, date_added=todo.date_added or datetime.datetime.utcnow()
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def toggle_todo_completion(db: Session, todo_id: int):
    db_todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if db_todo:
        db_todo.completed = not db_todo.completed
        db.commit()
        db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo
