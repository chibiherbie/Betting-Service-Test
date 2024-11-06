from enum import Enum, auto


class EventState(Enum):
    NEW = auto()
    FINISHED_WIN = auto()
    FINISHED_LOSE = auto()
