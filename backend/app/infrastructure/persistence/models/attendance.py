import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class SqlAttendance(Base):
    __tablename__ = "t_attendance"

    attendance_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(Uuid(as_uuid=True), ForeignKey("t_events.event_id"), nullable=False)
    email = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    join_time = Column(DateTime, nullable=True)
    leave_time = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=False) # minutes > 0, validated in schema/service
    role = Column(String, nullable=False) # e.g. attendee, speaker
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    event = relationship("SqlEvent", back_populates="attendance")
