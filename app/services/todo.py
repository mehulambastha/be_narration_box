from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from app.models.todo import Todo
from app.schemas.todo import TodoCreate
from .base import BaseService
from sqlalchemy import update
from ..sse.event_queue import emit_event


class TodoService(BaseService):
    async def create(self, todo_data: TodoCreate) -> Todo:
        new_todo = Todo(title=todo_data.title,
                        description=todo_data.description, time_estimate=todo_data.time_estimate)
        self.db.add(new_todo)
        await self.db.commit()
        await self.db.refresh(new_todo)
        await emit_event(new_todo)
        return new_todo

    async def get_all(self) -> list[Todo]:
        result = await self.db.execute(select(Todo))
        return result.scalars().all()

    async def get_by_id(self, id: int) -> Todo:
        result = await self.db.execute(select(Todo).where(Todo.id == id))
        todo = result.scalar_one_or_none()
        if not todo:
            raise NoResultFound(f"Todo with id: {id} not found!")
        return todo

    async def delete(self, todo_id: int):
        todo = await self.get_by_id(todo_id)
        if not todo:
            raise NoResultFound(f"Todo with id: {id} not found!")
        return todo
        await self.db.delete(todo)
        await self.db.commit()
        await emit_event({"type": "Achievement", "content": "Big Achievement."})
        return {"message": f"Todo with id {todo_id} deleted."}

    async def mark_as_complete(self, todo_id: int) -> Todo:
        stmt = (
            update(Todo)
            .where(Todo.id == todo_id)
            .values(completed=True)
            .returning(Todo)
        )

        try:
            result = await self.db.execute(stmt)
            await self.db.commit()
            todo = result.scalar_one()
            return todo
        except Exception as e:
            await self.db.rollback()
            raise e
