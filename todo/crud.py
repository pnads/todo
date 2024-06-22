from sqlalchemy.orm import Session

from todo.models import ToDo


def create_todo(db: Session, title: str):
    db_todo = ToDo(title=title)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todos(db: Session):
    return db.query(ToDo).all()


def toggle_todo(db: Session, todo_id: int):
    db_todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if db_todo:
        db_todo.completed = not db_todo.completed
        db.commit()
        db.refresh(db_todo)
        return db_todo
    return None


def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
        return True
    return False
