import uuid
import enum
from sqlalchemy import Column, String, Date, DateTime, Enum, ForeignKey, Text, Uuid, Integer, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class EventStatus(str, enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    CANCELLED = "CANCELLED"

class SqlEvent(Base):
    __tablename__ = "t_events"

    event_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_name = Column(String, nullable=False)
    event_description = Column(Text, nullable=True) # HTML allowed
    event_date = Column(Date, nullable=False)
    event_status = Column(Enum(EventStatus), default=EventStatus.TODO, nullable=False)
    organizing_team = Column(String, nullable=False)
    
    # Stats
    participants_count = Column(Integer, nullable=True)
    average_duration = Column(Float, nullable=True)
    
    # Foreign Keys
    created_by = Column(Uuid(as_uuid=True), ForeignKey("t_users.uid"), nullable=False)
    updated_by = Column(Uuid(as_uuid=True), ForeignKey("t_users.uid"), nullable=True) # Nullable if update separates from create? Spec says updated_by -> FK.
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    attendance = relationship("SqlAttendance", back_populates="event", cascade="all, delete-orphan")
