import uuid
from datetime import date, datetime
from app.domain.event import Event, EventStatus
from app.domain.user import User

def test_event_repository_save_and_get(event_repo):
    uid = uuid.uuid4()
    event = Event(
        event_id=uuid.uuid4(),
        event_name="Repo Test",
        event_date=date.today(),
        event_status=EventStatus.TODO,
        organizing_team="Team R",
        created_by=uid,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    saved_event = event_repo.save(event)
    assert saved_event.event_name == "Repo Test"
    
    fetched = event_repo.get_by_id(saved_event.event_id)
    assert fetched is not None
    assert fetched.event_name == "Repo Test"

def test_user_repository_save_and_get(user_repo):
    user = User(
        uid=uuid.uuid4(),
        username="repotest",
        first_name="Repo",
        last_name="Test",
        email="repo@test.com",
        country_code="US",
        roles=["admin"],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    saved_user = user_repo.save(user)
    assert saved_user.username == "repotest"
    
    fetched = user_repo.get_by_email("repo@test.com")
    assert fetched is not None
    assert fetched.username == "repotest"
