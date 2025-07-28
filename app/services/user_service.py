from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.crud import select_records, insert_record, update_records, delete_record
from app.exception import RecordNotFound, RecordExists
from fastapi import HTTPException, status


def create_user(db: Session, user_data: UserCreate):
    """Service method to create a user."""
    try:
        user_record = insert_record(
            db, User, name=user_data.name, email=user_data.email
        )
        db.commit()
        db.refresh(user_record)

        return {
            "user_id": user_record.id,
            "message": "Successfully created new user record",
        }
    except IntegrityError:
        db.rollback()
        raise RecordExists(
            msg="A user with this email already exists.",
        )


def get_user_by_id(db: Session, user_id: str):
    """Service method to retrieve a user by ID."""
    filter_conditions = [User.id == user_id]
    query = select_records(db, User, filter_conditions=filter_conditions)
    user = query.first()

    if not user:
        raise RecordNotFound(
            msg=f"User with ID {user_id} not found.",
        )
    return user


def get_users(db: Session, page: int, limit: int):
    """Service method to retrieve a list of users."""
    offset = (page - 1) * limit
    query = select_records(db, User, offset=offset, limit=limit)
    users = query.all()
    return users


def update_user(db: Session, user_id: str, updated_user_data: UserUpdate):
    """Service method to update a user's details."""
    try:
        get_user_by_id(db, user_id)  # Check whether user with ID exists
        filter_criteria = [User.id == user_id]
        records_to_update = updated_user_data.model_dump(exclude_unset=True)
        update_records(
            db,
            User,
            filter_criteria=filter_criteria,
            records_to_update=records_to_update,
        )
        db.commit()
        return {"user_id": user_id, "message": "Successfully updated user record"}
    except IntegrityError:
        db.rollback()
        raise RecordExists(
            msg="A user with this email already exists.",
        )


def delete_user(db: Session, user_id: str):
    """Service method to delete a user."""
    get_user_by_id(db, user_id)  # Check whether user with ID exists
    filter_criteria = [User.id == user_id]
    delete_record(db, User, filter_criteria)
    db.commit()
    return {"user_id": user_id, "message": "Successfully deleted user record"}
