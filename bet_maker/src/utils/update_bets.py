from sqlalchemy import update

from src.database import async_session_maker
from src.enums.bets_status import EVENT_TO_BET_STATUS
from src.enums.event_state import EventState
from src.models.bets import BetsOrm


async def update_bets(event_id: str, state: EventState) -> None:
    async with async_session_maker() as session:
        query = update(BetsOrm).filter_by(event_id=event_id).values(status=EVENT_TO_BET_STATUS[state])
        await session.execute(query)
        await session.commit()
