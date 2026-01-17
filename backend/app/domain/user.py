from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from app.domain.value_objects import UserId

class User(BaseModel):
    """
    Domain Entity representing a User.
    Decoupled from DB concerns (orm_mode, etc) and API concerns.
    """
    id: UserId = Field(alias="uid") 
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    country_code: str
    roles: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions or "admin" in self.roles
