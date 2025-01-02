from asyncio import Queue
from ..models.todo import Todo
import json
from ..schemas.todo import TodoResponse

event_queue = Queue()


async def emit_event(event_data):
    await event_queue.put(event_data)


async def handle_sse():
    event = await event_queue.get()
    if isinstance(event, Todo):
        return {"data": TodoResponse.from_orm(event).model_dump_json()}
    elif isinstance(event, dict) and "type" in event:
        return {"data": json.dumps(event)}
    else:
        return {"data": json.dumps(event)}
