from pydantic import BaseModel
from typing import Optional
from ..models.todo import Todo


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
    time_estimate: Optional[str] = None


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    pass


class TodoResponse(TodoBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True

    @staticmethod
    def from_orm(todo: Todo):
        return TodoResponse(
            id=todo.id,
            title=todo.title,  # Include the title
            description=todo.description,  # Include the description if applicable
            completed=todo.completed,
            created_at=todo.created_at.isoformat(),
            time_estimate=todo.time_estimate
        )


class TodoCondensedResponse(BaseModel):
    id: int
    created_at: str

    class Config:
        orm_mode = True

    @staticmethod
    def from_orm(todo: Todo):
        return TodoCondensedResponse(
            id=todo.id,
            created_at=todo.created_at.isoformat()
        )


class TaskRequest(BaseModel):
    prompt: str
    level: int
