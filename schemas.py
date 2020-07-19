from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional


class SessionBase(BaseModel):
    id: str
    state: str


class Session(SessionBase):
    klass_id: str
    room: str
    teacher: str
    subject: str
    actual_start_time: Optional[datetime.datetime]
    actual_end_time: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class SessionAttendanceAggregated(BaseModel):
    session_id: str
    present: int
    unknown: int
    total: int


class SessionPulseAggregated(BaseModel):
    session_id: str
    timestamp: datetime.datetime
    student_group_name: str
    attentiveness: int
    engagement: int


class Student(BaseModel):
    student_id: str
    name: Optional[str]
    current_grade: Optional[str]
    current_board: Optional[str]
    ref_image_urls: List[str]


class Teacher(BaseModel):
    teacher_id: str
    name: str
    email: str
    ref_image_urls: List[str]


class SessionIntervention(BaseModel):
    pass

