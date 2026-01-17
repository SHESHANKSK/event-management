from datetime import date
from typing import Optional
from pydantic import BaseModel
from app.domain.value_objects import UserId, EventId

class CreateEventCommand(BaseModel):
    event_name: str
    event_description: Optional[str] = None
    event_date: date
    organizing_team: str
    creator_id: UserId

class UpdateEventCommand(BaseModel):
    event_id: EventId
    event_name: Optional[str] = None
    event_description: Optional[str] = None
    event_date: Optional[date] = None
    organizing_team: Optional[str] = None
    updater_id: UserId

class CancelEventCommand(BaseModel):
    event_id: EventId
    user_id: UserId
