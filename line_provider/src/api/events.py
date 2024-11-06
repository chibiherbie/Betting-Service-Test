import decimal
import time
from typing import Dict

from fastapi import Path, HTTPException, status, APIRouter

from src.init import redis_manager
from src.shemas.events import Event

router = APIRouter(prefix="/events", tags=["События"])

events: Dict[str, Event] = {
    '1': Event(event_id='1', coefficient=decimal.Decimal("1.20"), deadline=int(time.time()) + 600),
    '2': Event(event_id='2', coefficient=decimal.Decimal("1.15"), deadline=int(time.time()) + 60),
    '3': Event(event_id='3', coefficient=decimal.Decimal("1.67"), deadline=int(time.time()) + 90)
}


@router.put('/event', status_code=status.HTTP_201_CREATED, summary="Создать или обновить событие")
async def create_or_update_event(event: Event):
    if event.event_id not in events:
        events[event.event_id] = event
        await redis_manager.publish_event_update(event)
        return {"message": "Event created"}

    for field, value in event.dict(exclude_unset=True).items():
        setattr(events[event.event_id], field, value)

    await redis_manager.publish_event_update(event)
    return {"message": "Event updated"}


@router.get('/event/{event_id}', summary="Получить информацию о событии")
async def get_event(event_id: str = Path(..., description="Уникальный идентификатор события")) -> Event:
    event = events.get(event_id)
    if event:
        return event
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")


@router.get('/events', summary="Получить список доступных событий")
async def get_active_events() -> list[Event]:
    return [event for event in events.values() if event.deadline > time.time()]
