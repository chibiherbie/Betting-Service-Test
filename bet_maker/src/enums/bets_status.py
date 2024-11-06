from enum import Enum, auto

from src.enums.event_state import EventState


class BetStatus(Enum):
    PENDING = auto()
    WIN = auto()
    LOSS = auto()


EVENT_TO_BET_STATUS = {
    EventState.NEW: BetStatus.PENDING,
    EventState.FINISHED_WIN: BetStatus.WIN,
    EventState.FINISHED_LOSE: BetStatus.LOSS,
}
