import uuid
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.persistence.database import get_db
from app.infrastructure.persistence.repositories import (
    SqlAlchemyEventRepository, 
    SqlAlchemyUserRepository,
    SqlAlchemyAttendanceRepository
)
from app.infrastructure.persistence.models.user import SqlUser
from app.application.use_cases.event_cases import EventUseCases
from app.application.use_cases.user_cases import UserUseCases
from app.application.use_cases.attendance_cases import AttendanceUseCases
from app.application.ports.repository import EventRepository, UserRepository, AttendanceRepository

# Mock Auth Dependency
MOCK_USER_ID = uuid.UUID("550e8400-e29b-41d4-a716-446655440000")

def get_current_active_user(db: Session = Depends(get_db)) -> SqlUser:
    user = db.query(SqlUser).filter(SqlUser.uid == MOCK_USER_ID).first()
    if not user:
        # Fallback if seed didn't run
        user = SqlUser(
            uid=MOCK_USER_ID,
            username="testadmin",
            first_name="Test",
            last_name="Admin",
            email="admin@internal.com",
            country_code="US",
            roles=["admin"]
        )
        # Not adding to DB here, just returning transient object for mock auth
    return user

# Dependency for Repositories
def get_event_repository(db: Session = Depends(get_db)) -> EventRepository:
    return SqlAlchemyEventRepository(db)

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return SqlAlchemyUserRepository(db)

def get_attendance_repository(db: Session = Depends(get_db)) -> AttendanceRepository:
    return SqlAlchemyAttendanceRepository(db)

# Dependency for Use Cases
def get_event_use_cases(repo: EventRepository = Depends(get_event_repository)) -> EventUseCases:
    return EventUseCases(repo)

def get_user_use_cases(repo: UserRepository = Depends(get_user_repository)) -> UserUseCases:
    return UserUseCases(repo)

def get_attendance_use_cases(
    attendance_repo: AttendanceRepository = Depends(get_attendance_repository),
    event_repo: EventRepository = Depends(get_event_repository)
) -> AttendanceUseCases:
    return AttendanceUseCases(attendance_repo, event_repo)
