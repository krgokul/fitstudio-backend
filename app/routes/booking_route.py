from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app import schemas, database
from app.services import booking_service

router = APIRouter(tags=["Fitness Class"])


@router.post(
    "/",
    response_model=schemas.BookingActionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_bookin_endpoint(
    booking_class_data: schemas.BookingCreate,
    db: Session = Depends(database.get_db),
):
    return booking_service.create_booking(db, booking_class_data)


@router.get(
    "/",
    response_model=List[schemas.BookingResponse],
    status_code=status.HTTP_200_OK,
)
def get_bookings_endpoint(
    email: Optional[str] = Query(None, description="Client email address"),
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(database.get_db),
):
    return booking_service.get_bookings(db, page=page, limit=limit, email=email)
