from pydantic import BaseModel, Field
from app.models.enums import Grade, Section, Curriculum
from typing import List, Optional
from app.schemas.student import StudentGroup


class School(BaseModel):
    name: str
    group_name: str
    location: str

    class Config:
        orm_mode = True


class Camera(BaseModel):
    name: str
    stream_url: Optional[str]
    position: Optional[str] = None

    class Config:
        orm_mode = True


class Room(BaseModel):
    name: str
    cameras: List[Camera]

    class Config:
        orm_mode = True


class Klass(BaseModel):
    grade: Grade
    section: Section
    curriculum: Curriculum
    student_groups: List[StudentGroup]

    class Config:
        orm_mode = True








