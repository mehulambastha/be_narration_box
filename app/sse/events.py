from pydantic import BaseModel
from collections import deque


class EventModel(BaseModel):
    type: str
    content: str


class SSEEvent:
    EVENTS = deque()

    @staticmethod
    def add_event(event: EventModel):
        SSEEvent.EVENTS.append(event)

    @staticmethod
    def get_event():
        if len(SSEEvent.EVENTS) > 0:
            return SSEEvent.EVENTS.popleft()
        return None

    @staticmethod
    def count():
        return len(SSEEvent.EVENTS)
