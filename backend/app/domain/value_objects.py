from enum import Enum
from uuid import UUID
from typing import NewType

# Value Objects
class EventStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    CANCELLED = "CANCELLED"

# Helper for strong typing if needed, though Pydantic handles UUID well.
EventId = UUID
UserId = UUID
