import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from todo.database import Base


class ToDo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)
    date_added = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
