import pytest
import uuid
from unittest.mock import MagicMock
from app.application.use_cases.user_cases import UserUseCases
from app.application.user_dtos import CreateUserCommand
from app.domain.user import User
from app.application.ports.repository import UserRepository
from datetime import datetime

@pytest.fixture
def mock_repo():
    return MagicMock(spec=UserRepository)

@pytest.fixture
def use_cases(mock_repo):
    return UserUseCases(mock_repo)

def test_create_user_success(use_cases, mock_repo):
    command = CreateUserCommand(
        username="newuser",
        first_name="First",
        last_name="Last",
        email="new@example.com",
        country_code="US",
        roles=["viewer"]
    )
    mock_repo.get_by_email.return_value = None
    mock_repo.save.side_effect = lambda x: x
    
    result = use_cases.create_user(command)
    
    assert result.username == "newuser"
    assert mock_repo.save.called

def test_create_user_already_exists(use_cases, mock_repo):
    command = CreateUserCommand(
        username="existing",
        first_name="First",
        last_name="Last",
        email="existing@example.com",
        country_code="US",
        roles=["viewer"]
    )
    # Return a real User domain entity
    mock_repo.get_by_email.return_value = User(
        uid=uuid.uuid4(),
        username="existing",
        first_name="Ex",
        last_name="Is",
        email="existing@example.com",
        country_code="US",
        roles=["viewer"],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    with pytest.raises(ValueError, match="already exists"):
        use_cases.create_user(command)
