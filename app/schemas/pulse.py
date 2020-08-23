from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.mongo_helpers import ObjectIdStr, LazyReferenceStr
from app.schemas.student import Student


class SessionAttendanceAggregated(BaseModel):
    present: int
    unknown: Optional[int] = 0
    total: int


class SessionAttendance(BaseModel):
    student: Student
    is_present: bool

    class Config:
        orm_mode = True


class SessionPulse(BaseModel):
    datetime_sequence: Optional[datetime]
    student_group_name: str
    attentiveness: int
    engagement: int

    class Config:
        orm_mode = True


class SessionPulseStudent(BaseModel):
    datetime_sequence: Optional[datetime]
    student_id: LazyReferenceStr = Field(alias='student')
    attentiveness: int
    engagement: int

    class Config:
        orm_mode = True


class SessionIntervention(BaseModel):

    class Config:
        orm_mode = True


class SessionPulseAggregated(BaseModel):
    engagement: int
    attentiveness: int

    class Config:
        orm_mode = True
