import httpx; print(f"DEBUG: httpx version: {httpx.__version__}")
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.infrastructure.persistence.database import Base, get_db
from app.presentation.web.dependencies import get_current_active_user
from app.infrastructure.persistence.models.user import SqlUser
import uuid

# Setup test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Mock Auth for all router tests
MOCK_USER_ID = uuid.UUID("550e8400-e29b-41d4-a716-446655440000")

def override_get_current_active_user():
    return SqlUser(
        uid=MOCK_USER_ID,
        username="testadmin",
        first_name="Test",
        last_name="Admin",
        email="admin@internal.com",
        country_code="US",
        roles=["admin"]
    )

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_active_user] = override_get_current_active_user

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True, scope="module")
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_read_events_empty(client):
    response = client.get("/events/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_event(client):
    event_data = {
        "event_name": "Integration Test Event",
        "event_description": "Testing the full flow",
        "event_date": "2026-05-20",
        "organizing_team": "QA Team"
    }
    response = client.post("/events/", json=event_data)
    assert response.status_code == 200
    data = response.json()
    assert data["event_name"] == "Integration Test Event"
    assert "event_id" in data

def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    # Might be empty or have seeded data depending on session start
    assert isinstance(response.json(), list)
