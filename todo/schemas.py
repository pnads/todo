import datetime

from pydantic import BaseModel


class ToDoCreate(BaseModel):
    title: str
    date_added: datetime.datetime = None
