import pytest
import uuid
from datetime import datetime
from app.domain.user import User

def test_user_full_name():
    user = User(
        uid=uuid.uuid4(),
        username="testuser",
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        country_code="US",
        roles=["viewer"],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    assert user.full_name == "John Doe"

def test_user_permissions():
    user = User(
        uid=uuid.uuid4(),
        username="admin",
        first_name="Admin",
        last_name="User",
        email="admin@example.com",
        country_code="US",
        roles=["admin"],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    # This assumes we have a way to map roles to permissions in the domain or just check roles
    assert "admin" in user.roles
