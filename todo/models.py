from sqlalchemy import Boolean, Column, Integer, String

from todo.database import Base


class ToDo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)
