from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from app.domain.value_objects import UserId, EventId
import uuid

class Attendance(BaseModel):
    """
    Domain Entity representing an Attendance record.
    Append-only record of a user's participation in an event.
    """
    attendance_id: uuid.UUID
    event_id: EventId
    email: EmailStr
    duration: int = Field(gt=0) # Duration in minutes
    role: str = "Attendee"
    full_name: Optional[str] = None
    join_time: Optional[datetime] = None
    leave_time: Optional[datetime] = None

    model_config = {"from_attributes": True}
