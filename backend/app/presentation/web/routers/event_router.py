from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.presentation.web.schemas.event import EventCreate, EventUpdate, EventResponse
from app.application.use_cases.event_cases import EventUseCases
from app.application.dtos import CreateEventCommand, UpdateEventCommand, CancelEventCommand
from app.presentation.web.dependencies import get_event_use_cases, get_current_active_user
from app.infrastructure.persistence.models.user import SqlUser

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/", response_model=EventResponse)
def create_event(
    event_in: EventCreate,
    use_cases: EventUseCases = Depends(get_event_use_cases),
    current_user: SqlUser = Depends(get_current_active_user)
):
    command = CreateEventCommand(
        event_name=event_in.event_name,
        event_description=event_in.event_description,
        event_date=event_in.event_date,
        organizing_team=event_in.organizing_team,
        creator_id=current_user.uid
    )
    return use_cases.create_event(command)

@router.get("/", response_model=List[EventResponse])
def read_events(
    skip: int = 0, 
    limit: int = 100, 
    use_cases: EventUseCases = Depends(get_event_use_cases)
):
    return use_cases.list_events(skip, limit)

@router.get("/{event_id}", response_model=EventResponse)
def read_event(
    event_id: str,
    use_cases: EventUseCases = Depends(get_event_use_cases)
):
    try:
        return use_cases.get_event(event_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: str,
    event_update: EventUpdate,
    use_cases: EventUseCases = Depends(get_event_use_cases),
    current_user: SqlUser = Depends(get_current_active_user)
):
    try:
        command = UpdateEventCommand(
            event_id=event_id,
            **event_update.model_dump(exclude_unset=True),
            updater_id=current_user.uid
        )
        return use_cases.update_event(command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{event_id}")
def cancel_event(
    event_id: str,
    use_cases: EventUseCases = Depends(get_event_use_cases),
    current_user: SqlUser = Depends(get_current_active_user)
):
    try:
        command = CancelEventCommand(event_id=event_id, user_id=current_user.uid)
        return use_cases.cancel_event(command)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
