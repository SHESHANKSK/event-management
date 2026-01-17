from pydantic import BaseModel, UUID4, Field, validator
from typing import Optional
from datetime import date, datetime
from app.presentation.web.schemas.common import EventStatus

class EventBase(BaseModel):
    event_name: str = Field(..., min_length=1)
    event_description: Optional[str] = None
    event_date: date
    organizing_team: str = Field(..., min_length=1)

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    event_name: Optional[str] = Field(None, min_length=1)
    event_description: Optional[str] = None
    event_date: Optional[date] = None
    # Status updates handled via specific logic or allowed here if transition valid?
    # Requirement: "Editing rules: Only allowed when status not in {DONE, CANCELLED}"
    # Status transitions might be separate or part of update. Let's include status but service layer validates.
    event_status: Optional[EventStatus] = None

class EventResponse(EventBase):
    event_id: UUID4
    event_status: EventStatus
    created_by: UUID4
    created_at: datetime
    updated_by: Optional[UUID4] = None
    updated_at: datetime
    participants_count: Optional[int] = None
    average_duration: Optional[float] = None

    model_config = {"from_attributes": True}
