from pydantic import BaseModel, EmailStr, UUID4, Field
from typing import List, Optional
from datetime import datetime

class AttendanceBase(BaseModel):
    email: EmailStr
    duration: int = Field(..., gt=0, description="Duration in minutes, must be > 0")
    role: str = Field(..., min_length=1)
    full_name: Optional[str] = None
    join_time: Optional[datetime] = None
    leave_time: Optional[datetime] = None

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    duration: Optional[int] = Field(None, gt=0)
    role: Optional[str] = Field(None, min_length=1)

class AttendanceBulkCreate(BaseModel):
    items: List[AttendanceCreate]

class AttendanceResponse(AttendanceBase):
    attendance_id: UUID4
    event_id: UUID4
    created_at: datetime
    full_name: Optional[str] = None
    join_time: Optional[datetime] = None
    leave_time: Optional[datetime] = None

    model_config = {"from_attributes": True}
