from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field

from app.schemas.mongo_helpers import LazyReferenceStr
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
    attentiveness: Optional[float]
    engagement: Optional[float]

    class Config:
        orm_mode = True


class SessionPulseStudent(BaseModel):
    datetime_sequence: Optional[datetime]
    student_id: LazyReferenceStr = Field(alias='student')
    attentiveness: Optional[float]
    engagement: Optional[float]

    class Config:
        orm_mode = True


class SessionIntervention(BaseModel):

    class Config:
        orm_mode = True


class SessionPulseAggregated(BaseModel):
    engagement: Optional[float]
    attentiveness: Optional[float]

    class Config:
        orm_mode = True


class SessionIntervention(BaseModel):
    datetime_created: Optional[datetime] = datetime.now()
    datetime_sequence: Optional[datetime] = datetime.now()
    version: Optional[str] = None
    intervention_reason: str
    intervention_period_start: datetime
    intervention_period_end: datetime
    intervention_reason_value: float
    intervention_reason_threshold: float
    student_group_name: Optional[str] = None
    student: Optional[Student] = None
    type: str = Field(alias='_cls')

    class Config:
        orm_mode = True


class StudentGroupIntervention(SessionIntervention):
    student_group_name: str

    class Config:
        orm_mode = True


class StudentIntervention(SessionIntervention):
    student: Student

    class Config:
        orm_mode = True


class SessionInterventionOut(BaseModel):
    intervention: Union[StudentIntervention, StudentGroupIntervention]

    class Config:
        orm_mode = True
