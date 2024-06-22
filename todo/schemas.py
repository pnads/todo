from pydantic import BaseModel


class ToDoCreate(BaseModel):
    title: str
