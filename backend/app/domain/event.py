from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.domain.value_objects import EventStatus, EventId, UserId

class Event(BaseModel):
    """
    Domain Entity representing an Event.
    Enforces invariants and encapsulates business logic for state transitions.
    """
    event_id: EventId
    event_name: str
    event_description: Optional[str] = None
    event_date: date
    event_status: EventStatus = EventStatus.TODO
    organizing_team: str
    
    # Stats (Domain logic might compute these, or they exist as state)
    participants_count: int = 0
    average_duration: float = 0.0
    
    # Audit
    created_by: UserId
    updated_by: Optional[UserId] = None
    created_at: datetime
    updated_at: datetime

    def cancel(self, user_id: UserId) -> None:
        """
        Business Rule: Events can be cancelled explicitly.
        """
        if self.event_status == EventStatus.CANCELLED:
            return
        
        self.event_status = EventStatus.CANCELLED
        self.updated_by = user_id
        self.updated_at = datetime.now()

    def update_details(self, name: str, description: str, team: str, date_val: date, user_id: UserId) -> None:
        """
        Business Rule: Editing allowed only when status not in {DONE, CANCELLED}
        """
        if self.event_status in [EventStatus.DONE, EventStatus.CANCELLED]:
            raise ValueError(f"Cannot edit event in {self.event_status.value} state")

        self.event_name = name
        self.event_description = description
        self.organizing_team = team
        self.event_date = date_val
        self.updated_by = user_id
        self.updated_at = datetime.now()

    def complete(self, user_id: UserId) -> None:
        """
        Mark event as DONE.
        """
        if self.event_status == EventStatus.CANCELLED:
            raise ValueError("Cannot complete a cancelled event")
            
        self.event_status = EventStatus.DONE
        self.updated_by = user_id
        self.updated_at = datetime.now()
