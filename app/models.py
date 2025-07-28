from sqlalchemy import Column, String, Integer, Date, Time, Enum, ForeignKey
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.orm import relationship
from app.database import Base
import uuid


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


class Instructor(Base):
    __tablename__ = "instructors"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    bio = Column(String)


class FitnessClass(Base):
    __tablename__ = "fitness_classes"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String)


class ClassSchedule(Base):
    __tablename__ = "class_schedules"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    class_id = Column(String, ForeignKey("classes.id"), nullable=False)
    instructor_id = Column(String, ForeignKey("instructors.id"), nullable=False)
    class_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    capacity = Column(Integer, nullable=False)


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    schedule_id = Column(String, ForeignKey("class_schedules.id"), nullable=False)
    booked_at = Column(Date, nullable=False)
