import pytest
import uuid
from unittest.mock import MagicMock
from datetime import datetime, date
from app.application.use_cases.event_cases import EventUseCases
from app.application.dtos import CreateEventCommand, UpdateEventCommand, CancelEventCommand
from app.domain.event import Event, EventStatus
from app.application.ports.repository import EventRepository

@pytest.fixture
def mock_repo():
    return MagicMock(spec=EventRepository)

@pytest.fixture
def use_cases(mock_repo):
    return EventUseCases(mock_repo)

def test_create_event_use_case(use_cases, mock_repo):
    uid = uuid.uuid4()
    command = CreateEventCommand(
        event_name="New Event",
        event_description="Desc",
        event_date=date.today(),
        organizing_team="Team X",
        creator_id=uid
    )
    
    mock_repo.save.side_effect = lambda x: x
    
    result = use_cases.create_event(command)
    
    assert result.event_name == "New Event"
    assert mock_repo.save.called

def test_get_event_not_found(use_cases, mock_repo):
    mock_repo.get_by_id.return_value = None
    with pytest.raises(ValueError, match="not found"):
        use_cases.get_event(uuid.uuid4())

def test_cancel_event_use_case(use_cases, mock_repo):
    uid = uuid.uuid4()
    event_id = uuid.uuid4()
    event = Event(
        event_id=event_id,
        event_name="To Cancel",
        event_date=date.today(),
        event_status=EventStatus.TODO,
        organizing_team="Team A",
        created_by=uid,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    mock_repo.get_by_id.return_value = event
    mock_repo.save.side_effect = lambda x: x
    
    command = CancelEventCommand(event_id=event_id, user_id=uid)
    result = use_cases.cancel_event(command)
    
    assert result.event_status == EventStatus.CANCELLED
    assert mock_repo.save.called
