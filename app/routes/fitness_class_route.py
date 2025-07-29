from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app import schemas, database
from app.services import fitness_class_service

router = APIRouter(tags=["Fitness Class"])


@router.post(
    "/",
    response_model=schemas.FitnessClassActionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_fitness_class(
    fitness_class_data: schemas.FitnessClassCreate,
    db: Session = Depends(database.get_db),
):
    return fitness_class_service.create_fitness_class(db, fitness_class_data)


@router.get(
    "/{fitness_class_id}",
    response_model=schemas.FitnessClassResponse,
    status_code=status.HTTP_200_OK,
)
def get_fitness_class(fitness_class_id: str, db: Session = Depends(database.get_db)):
    return fitness_class_service.get_fitness_class_by_id(db, fitness_class_id)


@router.get(
    "/",
    response_model=List[schemas.FitnessClassResponse],
    status_code=status.HTTP_200_OK,
)
def get_fitness_classs(
    page: int = 1, limit: int = 10, db: Session = Depends(database.get_db)
):
    return fitness_class_service.get_fitness_classes(db, page=page, limit=limit)


@router.put(
    "/{fitness_class_id}",
    response_model=schemas.FitnessClassActionResponse,
    status_code=status.HTTP_200_OK,
)
def update_fitness_class(
    fitness_class_id: str,
    updated_fitness_class_data: schemas.FitnessClassUpdate,
    db: Session = Depends(database.get_db),
):
    return fitness_class_service.update_fitness_class(
        db, fitness_class_id, updated_fitness_class_data
    )


@router.delete(
    "/{fitness_class_id}",
    response_model=schemas.FitnessClassActionResponse,
    status_code=status.HTTP_200_OK,
)
def delete_fitness_class(fitness_class_id: str, db: Session = Depends(database.get_db)):
    return fitness_class_service.delete_fitness_class(db, fitness_class_id)
