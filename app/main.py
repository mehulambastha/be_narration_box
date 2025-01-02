from fastapi import FastAPI
from app.api.routers.todos import router as todo_router
from app.models.todo import Base
from app.database import engine
from fastapi.middleware.cors import CORSMiddleware
from .sse.events import SSEEvent, EventModel
from sse_starlette.sse import EventSourceResponse
from fastapi import Request, Security
from .sse.event_queue import emit_event, event_queue, handle_sse
from .sse.verify import verify_api_key
import json
from .schemas.todo import TodoResponse

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(todo_router, prefix="/todos", tags=["todos"])


@app.post("/emit")
async def emit_http(event: EventModel, api_key: str = Security(verify_api_key)):
    await emit_event(event)
    return {"status": "sent"}


@app.get("/stream")
async def stream(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break

            try:
                data = await handle_sse()
                yield data
            except Exception as e:
                print("Stream error: ", e)
                break

    return EventSourceResponse(event_generator())
