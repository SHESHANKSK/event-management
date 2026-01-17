import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.presentation.web.schemas.user import UserResponse, UserCreate, UserUpdate
from app.application.use_cases.user_cases import UserUseCases
from app.application.user_dtos import CreateUserCommand, UpdateUserCommand, DeleteUserCommand
from app.presentation.web.dependencies import get_user_use_cases, get_current_active_user
from app.infrastructure.persistence.models.user import SqlUser

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/", response_model=List[UserResponse])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    use_cases: UserUseCases = Depends(get_user_use_cases)
):
    return use_cases.list_users(skip, limit)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: uuid.UUID, 
    use_cases: UserUseCases = Depends(get_user_use_cases)
):
    try:
        return use_cases.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate, 
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: SqlUser = Depends(get_current_active_user)
):
    command = CreateUserCommand(
        username=user_in.username,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        country_code=user_in.country_code,
        roles=user_in.roles
    )
    return use_cases.create_user(command)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: uuid.UUID, 
    user_update: UserUpdate, 
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: SqlUser = Depends(get_current_active_user)
):
    try:
        command = UpdateUserCommand(
            user_id=user_id,
            **user_update.model_dump(exclude_unset=True)
        )
        return use_cases.update_user(command)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(
    user_id: uuid.UUID, 
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: SqlUser = Depends(get_current_active_user)
):
    try:
        command = DeleteUserCommand(user_id=user_id)
        return use_cases.delete_user(command)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
