from datetime import datetime
import uuid
from typing import List, Optional

from app.domain.user import User
from app.application.ports.repository import UserRepository
from app.application.user_dtos import CreateUserCommand, UpdateUserCommand, DeleteUserCommand
from app.domain.value_objects import UserId

class UserUseCases:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, command: CreateUserCommand) -> User:
        if self.repository.get_by_email(command.email):
            raise ValueError(f"User with email {command.email} already exists")
            
        user = User(
            uid=uuid.uuid4(),
            username=command.username,
            first_name=command.first_name,
            last_name=command.last_name,
            email=command.email,
            country_code=command.country_code,
            roles=command.roles,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        return self.repository.save(user)

    def get_user(self, user_id: UserId) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return user

    def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.repository.get_all(skip, limit)

    def update_user(self, command: UpdateUserCommand) -> User:
        user = self.get_user(command.user_id)
        
        # Partially update based on command
        if command.first_name is not None:
            user.first_name = command.first_name
        if command.last_name is not None:
            user.last_name = command.last_name
        if command.email is not None:
            user.email = command.email
        if command.country_code is not None:
            user.country_code = command.country_code
        if command.roles is not None:
            user.roles = command.roles
        if command.is_active is not None:
            user.is_active = command.is_active
            
        user.updated_at = datetime.now()
        
        return self.repository.save(user)

    def delete_user(self, command: DeleteUserCommand) -> User:
        user = self.get_user(command.user_id)
        user.is_active = False
        user.updated_at = datetime.now()
        return self.repository.save(user)
