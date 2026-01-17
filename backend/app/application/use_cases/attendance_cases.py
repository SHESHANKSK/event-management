from typing import List
import uuid
from app.domain.attendance import Attendance
from app.domain.event import EventStatus
from app.application.ports.repository import AttendanceRepository, EventRepository
# No command DTO used currently for bulk attendance

class AttendanceUseCases:
    def __init__(self, attendance_repo: AttendanceRepository, event_repo: EventRepository):
        self.attendance_repo = attendance_repo
        self.event_repo = event_repo

    def get_attendance_by_event(self, event_id: uuid.UUID) -> List[Attendance]:
        return self.attendance_repo.get_by_event(event_id)

    def create_attendance(self, event_id: uuid.UUID, attendance_data: List[dict]) -> List[Attendance]:
        event = self.event_repo.get_by_id(event_id)
        if not event:
            raise ValueError("Event not found")
        
        if event.event_status == EventStatus.CANCELLED:
            raise ValueError("Cannot add attendance to a CANCELLED event")
        
        records = []
        for item in attendance_data:
            record = Attendance(
                attendance_id=uuid.uuid4(),
                event_id=event_id,
                **item
            )
            records.append(record)
        
        saved_records = self.attendance_repo.save_all(records)
        
        # Trigger event stats update
        self._update_event_stats(event_id)
        
        return saved_records

    def _update_event_stats(self, event_id: uuid.UUID):
        records = self.attendance_repo.get_by_event(event_id)
        event = self.event_repo.get_by_id(event_id)
        if event and records:
            event.participants_count = len(records)
            event.average_duration = round(sum(r.duration for r in records) / len(records), 2)
            self.event_repo.save(event)
