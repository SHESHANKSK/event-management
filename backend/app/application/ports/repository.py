import uuid
from typing import List, Optional, Protocol
from app.domain.event import Event
from app.domain.user import User
from app.domain.attendance import Attendance
from app.domain.value_objects import EventId, UserId

class EventRepository(Protocol):
    def save(self, event: Event) -> Event:
        """Save an event (create or update)."""
        ...
    
    def get_by_id(self, event_id: EventId) -> Optional[Event]:
        """Retrieve an event by ID."""
        ...
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Event]:
        """Retrieve all events with pagination."""
        ...

class UserRepository(Protocol):
    def save(self, user: User) -> User:
        """Save a user."""
        ...
    
    def get_by_id(self, user_id: UserId) -> Optional[User]:
        """Retrieve a user by ID."""
        ...
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by email."""
        ...

class AttendanceRepository(Protocol):
    def save_all(self, attendance_list: List[Attendance]) -> List[Attendance]:
        """Save a list of attendance records."""
        ...
    
    def get_by_event(self, event_id: EventId) -> List[Attendance]:
        """Retrieve all attendance records for an event."""
        ...
    
    def get_by_id(self, attendance_id: uuid.UUID) -> Optional[Attendance]:
        """Retrieve a specific attendance record."""
        ...
