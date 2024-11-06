from pydantic import BaseModel, Field, condecimal

from src.enums.bets_status import BetStatus


class BetCreate(BaseModel):
    event_id: str
    amount: condecimal(gt=0, max_digits=4, decimal_places=2) = Field(..., description="Сумма ставки")


class BetResponse(BetCreate):
    id: int
    status: BetStatus
