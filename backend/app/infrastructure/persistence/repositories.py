import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.event import Event
from app.domain.user import User
from app.domain.attendance import Attendance
from app.domain.value_objects import EventId, UserId
from app.application.ports.repository import EventRepository, UserRepository, AttendanceRepository
from app.infrastructure.persistence.models import SqlEvent, SqlUser, SqlAttendance
from app.infrastructure.persistence.mappers import (
    event_to_domain, event_to_persistence,
    user_to_domain, user_to_persistence,
    attendance_to_domain, attendance_to_persistence
)

class SqlAlchemyEventRepository(EventRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, event: Event) -> Event:
        existing = self.db.query(SqlEvent).filter(SqlEvent.event_id == event.event_id).first()
        orm_data = event_to_persistence(event)
        
        if existing:
            existing.event_name = orm_data.event_name
            existing.event_description = orm_data.event_description
            existing.event_status = orm_data.event_status
            existing.event_date = orm_data.event_date
            existing.organizing_team = orm_data.organizing_team
            existing.updated_by = orm_data.updated_by
            existing.updated_at = orm_data.updated_at
            existing.participants_count = orm_data.participants_count
            existing.average_duration = orm_data.average_duration
            self.db.add(existing)
            self.db.commit()
            self.db.refresh(existing)
            return event_to_domain(existing)
        else:
            self.db.add(orm_data)
            self.db.commit()
            self.db.refresh(orm_data)
            return event_to_domain(orm_data)

    def get_by_id(self, event_id: EventId) -> Optional[Event]:
        sql_event = self.db.query(SqlEvent).filter(SqlEvent.event_id == event_id).first()
        if sql_event:
            return event_to_domain(sql_event)
        return None

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Event]:
        sql_events = self.db.query(SqlEvent).offset(skip).limit(limit).all()
        return [event_to_domain(e) for e in sql_events]

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User) -> User:
        existing = self.db.query(SqlUser).filter(SqlUser.uid == user.id).first()
        orm_data = user_to_persistence(user)
        
        if existing:
            existing.first_name = orm_data.first_name
            existing.last_name = orm_data.last_name
            existing.email = orm_data.email
            existing.country_code = orm_data.country_code
            existing.roles = orm_data.roles
            existing.is_active = orm_data.is_active
            existing.updated_at = orm_data.updated_at
            self.db.add(existing)
            self.db.commit()
            self.db.refresh(existing)
            return user_to_domain(existing)
        else:
            self.db.add(orm_data)
            self.db.commit()
            self.db.refresh(orm_data)
            return user_to_domain(orm_data)

    def get_by_id(self, user_id: UserId) -> Optional[User]:
        sql_user = self.db.query(SqlUser).filter(SqlUser.uid == user_id).first()
        if sql_user:
            return user_to_domain(sql_user)
        return None

    def get_by_email(self, email: str) -> Optional[User]:
        sql_user = self.db.query(SqlUser).filter(SqlUser.email == email).first()
        if sql_user:
            return user_to_domain(sql_user)
        return None

    def get_by_username(self, username: str) -> Optional[User]:
        sql_user = self.db.query(SqlUser).filter(SqlUser.username == username).first()
        if sql_user:
            return user_to_domain(sql_user)
        return None
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        sql_users = self.db.query(SqlUser).offset(skip).limit(limit).all()
        return [user_to_domain(u) for u in sql_users]

class SqlAlchemyAttendanceRepository(AttendanceRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_all(self, attendance_list: List[Attendance]) -> List[Attendance]:
        orm_records = [attendance_to_persistence(a) for a in attendance_list]
        for record in orm_records:
            self.db.add(record)
        self.db.commit()
        for record in orm_records:
            self.db.refresh(record)
        return [attendance_to_domain(r) for r in orm_records]

    def get_by_event(self, event_id: uuid.UUID) -> List[Attendance]:
        orm_records = self.db.query(SqlAttendance).filter(SqlAttendance.event_id == event_id).all()
        return [attendance_to_domain(r) for r in orm_records]

    def get_by_id(self, attendance_id: uuid.UUID) -> Optional[Attendance]:
        orm_record = self.db.query(SqlAttendance).filter(SqlAttendance.attendance_id == attendance_id).first()
        if orm_record:
            return attendance_to_domain(orm_record)
        return None
