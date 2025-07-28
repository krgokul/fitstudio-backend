from pydantic import BaseModel
from datetime import date, time
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
