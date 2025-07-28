from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app import schemas, database
from app.services import user_service

router = APIRouter()


@router.post(
    "/", response_model=schemas.UserActionResponse, status_code=status.HTTP_201_CREATED
)
def create_user(user_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return user_service.create_user(db, user_data)


@router.get(
    "/{user_id}",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_200_OK,
)
def get_user(user_id: str, db: Session = Depends(database.get_db)):
    return user_service.get_user_by_id(db, user_id)


@router.get(
    "/", response_model=List[schemas.UserResponse], status_code=status.HTTP_200_OK
)
def get_users(page: int = 1, limit: int = 10, db: Session = Depends(database.get_db)):
    return user_service.get_users(db, page=page, limit=limit)


@router.put(
    "/{user_id}",
    response_model=schemas.UserActionResponse,
    status_code=status.HTTP_200_OK,
)
def update_user(
    user_id: str,
    updated_user_data: schemas.UserUpdate,
    db: Session = Depends(database.get_db),
):
    return user_service.update_user(db, user_id, updated_user_data)


@router.delete(
    "/{user_id}",
    response_model=schemas.UserActionResponse,
    status_code=status.HTTP_200_OK,
)
def delete_user(user_id: str, db: Session = Depends(database.get_db)):
    return user_service.delete_user(db, user_id)
