from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    Time,
    Enum,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.orm import relationship
from app.database import Base
import uuid


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


class FitnessClass(Base):
    __tablename__ = "fitness_classes"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    instructor = Column(String, nullable=False)
    class_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    available_slots = Column(Integer, nullable=False)
    description = Column(String)

    __table_args__ = (
        UniqueConstraint(
            "instructor", "class_date", "start_time", name="uix_instructor_schedule"
        ),
    )


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    class_id = Column(String, ForeignKey("fitness_classes.id"), nullable=False)
    booked_at = Column(Date, nullable=False)

    user = relationship("User")
    fitness_class = relationship("FitnessClass")

    __table_args__ = (
        UniqueConstraint("user_id", "class_id", name="uix_user_class_booking"),
    )
