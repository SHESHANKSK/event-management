import uuid
from datetime import datetime
from typing import List

from app.domain.event import Event, EventStatus
from app.application.ports.repository import EventRepository
from app.application.dtos import CreateEventCommand, UpdateEventCommand, CancelEventCommand
from app.domain.value_objects import EventId

class EventUseCases:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    def create_event(self, command: CreateEventCommand) -> Event:
        # Factory logic could be in Domain Service or static method on Entity, 
        # but simple creation defaults here are fine.
        event = Event(
            event_id=uuid.uuid4(),
            event_name=command.event_name,
            event_description=command.event_description,
            event_date=command.event_date,
            organizing_team=command.organizing_team,
            event_status=EventStatus.TODO,
            created_by=command.creator_id,
            updated_by=command.creator_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        return self.repository.save(event)

    def get_event(self, event_id: EventId) -> Event:
        event = self.repository.get_by_id(event_id)
        if not event:
            raise ValueError(f"Event with id {event_id} not found")
        return event

    def list_events(self, skip: int = 0, limit: int = 100) -> List[Event]:
        return self.repository.get_all(skip, limit)

    def update_event(self, command: UpdateEventCommand) -> Event:
        event = self.get_event(command.event_id)
        
        # Merge logic if fields are provided
        name = command.event_name if command.event_name is not None else event.event_name
        description = command.event_description if command.event_description is not None else event.event_description
        team = command.organizing_team if command.organizing_team is not None else event.organizing_team
        date_val = command.event_date if command.event_date is not None else event.event_date

        # Domain method encapsulates the update logic & invariants
        event.update_details(
            name=name,
            description=description,
            team=team,
            date_val=date_val,
            user_id=command.updater_id
        )
        
        return self.repository.save(event)

    def cancel_event(self, command: CancelEventCommand) -> Event:
        event = self.get_event(command.event_id)
        
        event.cancel(user_id=command.user_id)
        
        return self.repository.save(event)
