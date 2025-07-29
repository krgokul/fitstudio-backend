from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models import FitnessClass
from app.schemas import FitnessClassCreate, FitnessClassUpdate
from app.crud import select_records, insert_record, update_records, delete_record
from app.exception import RecordNotFound, RecordExists
from fastapi import HTTPException, status


def create_fitness_class(db: Session, fitness_class_data: FitnessClassCreate):
    """Service method to create a fitness class."""
    try:
        fitness_class_record = FitnessClass(
            **fitness_class_data.model_dump(exclude_unset=True)
        )
        db.add(fitness_class_record)
        db.commit()
        db.refresh(fitness_class_record)

        return {
            "fitness_class_id": fitness_class_record.id,
            "message": "Successfully created new fitness class record",
        }
    except IntegrityError:
        db.rollback()
        raise RecordExists(msg="Instructor is already scheduled at that date and time")


def get_fitness_class_by_id(db: Session, fitness_class_id: str):
    """Service method to retrieve a fitness class by ID."""
    filter_conditions = [FitnessClass.id == fitness_class_id]
    query = select_records(db, FitnessClass, filter_conditions=filter_conditions)
    fitness_class = query.first()

    if not fitness_class:
        raise RecordNotFound(
            msg=f"Fitness class with ID {fitness_class_id} not found.",
        )
    return fitness_class


def get_fitness_classes(db: Session, page: int, limit: int):
    """Service method to retrieve a list of fitness_classs."""
    offset = (page - 1) * limit
    query = select_records(db, FitnessClass, offset=offset, limit=limit)
    fitness_classs = query.all()
    return fitness_classs


def update_fitness_class(
    db: Session, fitness_class_id: str, updated_fitness_class_data: FitnessClassUpdate
):
    """Service method to update a fitness class's details."""
    try:
        get_fitness_class_by_id(
            db, fitness_class_id
        )  # Check whether fitness class with ID exists
        filter_criteria = [FitnessClass.id == fitness_class_id]
        records_to_update = updated_fitness_class_data.model_dump(exclude_unset=True)
        update_records(
            db,
            FitnessClass,
            filter_criteria=filter_criteria,
            records_to_update=records_to_update,
        )
        db.commit()
        return {
            "fitness_class_id": fitness_class_id,
            "message": "Successfully updated fitness class record",
        }
    except IntegrityError:
        db.rollback()
        raise RecordExists(
            msg="A fitness class with this email already exists.",
        )


def delete_fitness_class(db: Session, fitness_class_id: str):
    """Service method to delete a fitness class."""
    get_fitness_class_by_id(
        db, fitness_class_id
    )  # Check whether fitness class with ID exists
    filter_criteria = [FitnessClass.id == fitness_class_id]
    delete_record(db, FitnessClass, filter_criteria)
    db.commit()
    return {
        "fitness_class_id": fitness_class_id,
        "message": "Successfully deleted fitness class record",
    }
