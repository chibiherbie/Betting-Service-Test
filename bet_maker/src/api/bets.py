import time
from typing import Dict

from fastapi import HTTPException, APIRouter
from sqlalchemy import select
from starlette import status

from src.api.dependecies import SessionDep
from src.models.bets import BetsOrm
from src.shemas.bets import BetResponse, BetCreate
from src.shemas.events import Event

router = APIRouter(prefix="/bets", tags=["Ставки"])

events_cache: Dict[str, Event] = {}


@router.post("/bet", status_code=status.HTTP_201_CREATED, summary="Сделать ставку на событие")
async def create_bet(bet: BetCreate, db: SessionDep) -> BetResponse:
    event = events_cache.get(bet.event_id)
    if event is None or event.deadline < time.time():
        raise HTTPException(404)

    new_bet = BetsOrm(event_id=bet.event_id, amount=bet.amount)

    db.add(new_bet)
    await db.commit()
    await db.refresh(new_bet)
    return BetResponse.model_validate(new_bet, from_attributes=True)


@router.get("/bets", summary="Получить список всех ставок")
async def get_bets(db: SessionDep) -> list[BetResponse]:
    result = await db.execute(select(BetsOrm))
    return [BetResponse.model_validate(model, from_attributes=True) for model in result.scalars().all()]


@router.get('/events', summary="Получить список доступных событий")
async def get_active_events() -> list[Event]:
    return [event for event in events_cache.values() if event.deadline > time.time()]
