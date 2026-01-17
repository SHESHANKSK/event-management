import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from app.presentation.web.schemas.attendance import AttendanceResponse, AttendanceCreate
from app.application.use_cases.attendance_cases import AttendanceUseCases
from app.presentation.web.dependencies import get_attendance_use_cases
from app.infrastructure.parsers.csv_parser import parse_teams_csv

router = APIRouter(
    prefix="/attendance",
    tags=["attendance"]
)

@router.get("/event/{event_id}", response_model=List[AttendanceResponse])
def read_attendance_by_event(
    event_id: uuid.UUID, 
    use_cases: AttendanceUseCases = Depends(get_attendance_use_cases)
):
    return use_cases.get_attendance_by_event(event_id)

@router.post("/upload/{event_id}", response_model=List[AttendanceResponse])
async def upload_attendance(
    event_id: uuid.UUID,
    file: UploadFile = File(...),
    use_cases: AttendanceUseCases = Depends(get_attendance_use_cases)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    parsed_data = await parse_teams_csv(file)
    
    if not parsed_data:
        raise HTTPException(status_code=400, detail="No valid records found in CSV")

    try:
        return use_cases.create_attendance(event_id, parsed_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
