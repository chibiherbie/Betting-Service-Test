from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

from src.enums.bets_status import BetStatus


class BetsOrm(Base):
    __tablename__ = "bets"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    event_id: Mapped[str]
    amount: Mapped[Decimal]
    status = mapped_column(Enum(BetStatus), default=BetStatus.PENDING)
