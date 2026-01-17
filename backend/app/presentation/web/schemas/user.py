from pydantic import BaseModel, EmailStr, UUID4, Field
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    first_name: str
    last_name: str
    email: EmailStr
    country_code: str
    roles: List[str] = []

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    country_code: Optional[str] = None
    roles: Optional[List[str]] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    uid: UUID4
    is_active: bool
    created_at: datetime
    updated_at: datetime
    permissions: List[str] = []

    model_config = {"from_attributes": True}
