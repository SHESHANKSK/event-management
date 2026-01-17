import uuid
from datetime import datetime
from typing import Optional

from app.domain.event import Event
from app.domain.user import User
from app.domain.attendance import Attendance
from app.infrastructure.persistence.models import SqlEvent, SqlUser, SqlAttendance

def event_to_domain(sql_event: SqlEvent) -> Event:
    return Event(
        event_id=sql_event.event_id,
        event_name=sql_event.event_name,
        event_description=sql_event.event_description,
        event_date=sql_event.event_date,
        event_status=sql_event.event_status,
        organizing_team=sql_event.organizing_team,
        participants_count=sql_event.participants_count or 0,
        average_duration=sql_event.average_duration or 0.0,
        created_by=sql_event.created_by,
        updated_by=sql_event.updated_by,
        created_at=sql_event.created_at,
        updated_at=sql_event.updated_at
    )

def event_to_persistence(domain_event: Event) -> SqlEvent:
    return SqlEvent(
        event_id=domain_event.event_id,
        event_name=domain_event.event_name,
        event_description=domain_event.event_description,
        event_date=domain_event.event_date,
        event_status=domain_event.event_status,
        organizing_team=domain_event.organizing_team,
        participants_count=domain_event.participants_count,
        average_duration=domain_event.average_duration,
        created_by=domain_event.created_by,
        updated_by=domain_event.updated_by,
        created_at=domain_event.created_at,
        updated_at=domain_event.updated_at
    )

def user_to_domain(sql_user: SqlUser) -> User:
    return User(
        uid=sql_user.uid,
        username=sql_user.username,
        first_name=sql_user.first_name,
        last_name=sql_user.last_name,
        email=sql_user.email,
        country_code=sql_user.country_code,
        roles=sql_user.roles or [],
        is_active=sql_user.is_active,
        created_at=sql_user.created_at,
        updated_at=sql_user.updated_at
    )

def user_to_persistence(domain_user: User) -> SqlUser:
    return SqlUser(
        uid=domain_user.id,
        username=domain_user.username,
        first_name=domain_user.first_name,
        last_name=domain_user.last_name,
        email=domain_user.email,
        country_code=domain_user.country_code,
        roles=domain_user.roles,
        is_active=domain_user.is_active,
        created_at=domain_user.created_at,
        updated_at=domain_user.updated_at
    )

def attendance_to_domain(sql_attendance: SqlAttendance) -> Attendance:
    return Attendance(
        attendance_id=sql_attendance.attendance_id,
        event_id=sql_attendance.event_id,
        email=sql_attendance.email,
        duration=sql_attendance.duration,
        role=sql_attendance.role,
        full_name=sql_attendance.full_name,
        join_time=sql_attendance.join_time,
        leave_time=sql_attendance.leave_time
    )

def attendance_to_persistence(domain_attendance: Attendance) -> SqlAttendance:
    return SqlAttendance(
        attendance_id=domain_attendance.attendance_id,
        event_id=domain_attendance.event_id,
        email=domain_attendance.email,
        duration=domain_attendance.duration,
        role=domain_attendance.role,
        full_name=domain_attendance.full_name,
        join_time=domain_attendance.join_time,
        leave_time=domain_attendance.leave_time
    )
