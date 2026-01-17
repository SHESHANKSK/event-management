from typing import List, Optional
import uuid
from pydantic import BaseModel, EmailStr
from app.domain.value_objects import UserId

class CreateUserCommand(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    country_code: str
    roles: List[str] = []

class UpdateUserCommand(BaseModel):
    user_id: UserId
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    country_code: Optional[str] = None
    roles: Optional[List[str]] = None
    is_active: Optional[bool] = None

class DeleteUserCommand(BaseModel):
    user_id: UserId
