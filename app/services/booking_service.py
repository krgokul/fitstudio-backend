from datetime import date
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models import Booking, FitnessClass, User
from app.schemas import BookingCreate, BookingActionResponse, BookingResponse
from app.crud import select_records, insert_record, update_records, delete_record
from app.exception import RecordNotFound, RecordExists, BadRequestException
from app.services import fitness_class_service


def create_booking(db: Session, booking: BookingCreate):
    try:
        # Check if class exists
        fitness_class = fitness_class_service.get_fitness_class_by_id(
            db, booking.class_id
        )

        if fitness_class.available_slots == 0:
            raise BadRequestException(msg="No slots available")

        new_booking = Booking(
            user_id=booking.user_id, class_id=booking.class_id, booked_at=date.today()
        )
        fitness_class.available_slots -= 1
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)

        return {
            "booking_id": new_booking.id,
            "message": "Successfully created new booking record",
        }

    except IntegrityError as err:
        db.rollback()
        print(err)
        raise RecordExists(msg="You have already reserved a spot in this fitness class")


def get_bookings(db: Session, page: int, limit: int, email: str = None):
    """Service method to retrieve a list of bookings."""
    offset = (page - 1) * limit
    join_conditions = [(User, User.id == Booking.user_id)]
    filter_conditions = []
    if email:
        filter_conditions.append(User.email == email)

    query = select_records(
        db,
        Booking,
        join_conditions=join_conditions,
        filter_conditions=filter_conditions,
        offset=offset,
        limit=limit,
    )
    bookings = query.all()
    return bookings
