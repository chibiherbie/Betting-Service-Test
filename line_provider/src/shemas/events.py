from pydantic import BaseModel, Field, condecimal

from src.enums.event_state import EventState


class Event(BaseModel):
    event_id: str
    coefficient: condecimal(gt=0, max_digits=4, decimal_places=2) = Field(..., description="Коэффициент ставки")
    deadline: int = Field(..., description="Дата и время, до которого можно делать ставки")
    state: EventState = EventState.NEW
