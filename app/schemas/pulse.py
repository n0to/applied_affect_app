from datetime import datetime
from typing import Optional
from pydantic import BaseModel
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
    timestamp: Optional[datetime]
    student_group_name: Optional[str]
    attentiveness: int
    engagement: int

    class Config:
        orm_mode = True


class SessionPulseStudent(BaseModel):
    timestamp: Optional[datetime]
    student: Student
    attentiveness: int
    engagement: int

    class Config:
        orm_mode = True


class SessionIntervention(BaseModel):

    class Config:
        orm_mode = True



