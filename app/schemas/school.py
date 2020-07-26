from pydantic import BaseModel, Field
from app.models.enum_models import Grade, Section, Curriculum
from typing import List, Optional


class Klass(BaseModel):
    grade: Grade
    section: Section
    curriculum: Curriculum

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



