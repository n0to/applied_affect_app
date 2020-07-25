from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.enum_models import Scenario, Subject
from app.schemas.teacher import Teacher


class SessionConfiguration(BaseModel):
    timestamp: Optional[datetime] = Field(None, description="add description")
    th_min_student_for_int: Optional[float] = Field(None, title="Threshold")
    th_min_gap_bet_int: Optional[int] = Field(None, title="Threshold")
    th_min_gap_for_student_int: Optional[int] = Field(None, title="Threshold")


class SessionScenario(BaseModel):
    timestamp: Optional[datetime] = Field(None, title="Timestamp")
    scenario: Optional[Scenario] = Field(None, title="State scenario")


class SessionCreate(BaseModel):
    klass: str
    room: str
    subject: Subject
    teacher: Teacher
    scheduled_start_time: datetime
    scheduled_end_time: datetime
    scenarios: Optional[List[SessionScenario]] = Field(None, title="List of scenarios")
    configs: Optional[List[SessionConfiguration]] = Field(None, title="List of configurations")


class Session(SessionCreate):
    id: str
    actual_start_time: Optional[datetime]
    actual_end_time: Optional[datetime]
    video_url: Optional[List[str]]


class Student(BaseModel):
    student_id: str
    name: Optional[str]
    current_grade: Optional[str]
    current_board: Optional[str]
    ref_image_urls: List[str]


class SessionIntervention(BaseModel):
    pass

