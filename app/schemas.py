from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime, time
from typing import Optional


# User Schemas
class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    """Schema for creating a user."""

    pass


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    name: Optional[str] = None
    email: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response."""

    id: str
    model_config = {"from_attributes": True}


class UserActionResponse(BaseModel):
    """Schema for user action response."""

    user_id: str
    message: str


# User Schemas
class FitnessClassBase(BaseModel):
    name: str
    description: str = Field(default="")
    class_date: date
    start_time: time
    instructor: str
    available_slots: int = Field(ge=0, le=1000)


class FitnessClassCreate(FitnessClassBase):
    """Schema for creating a fitness class."""

    pass


class FitnessClassUpdate(BaseModel):
    """Schema for updating a user."""

    name: Optional[str] = None
    description: Optional[str] = None
    class_date: Optional[date] = None
    start_time: Optional[time] = None
    instructor: Optional[str] = None
    available_slots: Optional[int] = Field(default=None, ge=0, le=1000)


class FitnessClassResponse(FitnessClassBase):
    """Schema for fitness class response."""

    id: str
    model_config = {"from_attributes": True}


class FitnessClassActionResponse(BaseModel):
    """Schema for fitness class action response."""

    fitness_class_id: str
    message: str
