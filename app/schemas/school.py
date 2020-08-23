from pydantic import AnyUrl
from app.models.enums import Grade, Section, Curriculum
from typing import List, Optional
from app.schemas.mongo_helpers import ObjectIdStr
from app.schemas.student import StudentGroup, Student
from pydantic import BaseModel


class School(BaseModel):
    id: ObjectIdStr
    name: str
    group_name: str
    location: str

    class Config:
        orm_mode = True


class Camera(BaseModel):
    id: ObjectIdStr
    name: str
    stream_url: Optional[AnyUrl]
    position: Optional[str] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class Room(BaseModel):
    id: ObjectIdStr
    name: str
    cameras: List[Camera]

    class Config:
        orm_mode = True


class KlassWithoutStudentList(BaseModel):
    id: ObjectIdStr
    grade: Grade
    section: Section
    curriculum: Curriculum

    class Config:
        orm_mode = True


class Klass(KlassWithoutStudentList):
    student_groups: Optional[List[StudentGroup]] = []
    members: List[Student]

    class Config:
        orm_mode = True
