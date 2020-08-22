from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.enums import Grade, Curriculum
from app.schemas.user import User


class Student(User):
    student_id: Optional[str]
    grade: Optional[Grade]
    curriculum: Optional[Curriculum]
    is_opt_out_individual: Optional[bool] = Field(None, description="description here")
    is_opt_out_aggregate: Optional[bool] = Field(None, description="description here")

    class Config:
        orm_mode = True


class Guardian(User):
    students: List[Student]

    class Config:
        orm_mode = True


class StudentGroup(BaseModel):
    name: str
    members: Optional[List[Student]] = None

    class Config:
        orm_mode = True


class StudentAttendanceAggregated(BaseModel):
    present: int
    total: int


class StudentPulseAggregated(BaseModel):
    attentiveness: int
    engagement: int


class StudentSessionPulse(BaseModel):
    attentiveness: int
    engagement: int
    scenario: str
    datetime_sequence: datetime
