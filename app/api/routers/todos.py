from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound

from app.schemas.todo import TodoCreate, TodoResponse, TodoCondensedResponse, TaskRequest
from app.services.todo import TodoService
from app.models.todo import Todo
from app.database import get_db
from ...services.base import get_service
from ..llm.gen_todo import geneate_todos

router = APIRouter()


@router.post("/", response_model=TodoResponse)
async def create_todo(
    tood: TodoCreate,
    service: TodoService = Depends(get_service(TodoService))
):
    print("data recieved: ", tood)
    todo = await service.create(tood)
    print("AARAYa hAI BHENCOHD", todo.created_at, type(todo.created_at))
    return TodoResponse.from_orm(todo)


@router.get("/", response_model=list[TodoResponse])
async def get_todos(
        service: TodoService = Depends(get_service(TodoService))
):
    todos = await service.get_all()
    return [TodoResponse.from_orm(todo) for todo in todos]


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
        todo_id: int,
        service: TodoService = Depends(get_service(TodoService))
):
    try:
        todo = await service.get_by_id(todo_id)
        return TodoResponse.from_orm(todo)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Todo with it {
                            todo_id} not found!")


@router.delete("/delete/{todo_id}")
async def delete_todo(
    todo_id: int,
    service: TodoService = Depends(get_service(TodoService))
):
    try:
        return await service.delete(todo_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Todo with id {
                            todo_id} does not eist!")


@router.put("/complete/{todo_id}")
async def mark_as_complete(
    todo_id: int,
    service: TodoService = Depends(get_service(TodoService))
):
    try:
        result = await service.mark_as_complete(todo_id)
        return TodoResponse.from_orm(result)
    except NoResultFound:
        raise NoResultFound(f"Todo with id {todo_id} not found!")


@router.post("/generate")
async def generate_todos(
    request: TaskRequest,
    service: TodoService = Depends(get_service(TodoService))
):
    try:
        tasks = await geneate_todos(request.prompt, request.level)
        for task in tasks:
            db_task = TodoCreate(**task)
            try:
                print("task aayo ji: ", db_task)
                await service.create(db_task)
            except:
                print("Error while autogenerating tasks")

        return tasks
    except EnvironmentError:
        raise HTTPException(
            status_code=404, detail="Couldn't find the system prompt")
