from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.enum_models import Scenario, Subject, SessionState
from app.schemas.school import Klass, Room
from app.schemas.teacher import Teacher


class SessionConfiguration(BaseModel):
    th_min_student_for_int: Optional[int] = Field(None, description="Description Here")
    th_min_gap_bet_int: Optional[int] = Field(None, description="Description Here")
    th_min_gap_for_student_int: Optional[int] = Field(None, description="Description Here")
    timestamp: Optional[datetime] = Field(None, description="Description Here")

    class Config:
        orm_mode = True


class SessionScenario(BaseModel):
    name: Scenario = Field(None, title="State scenario")
    timestamp: Optional[datetime] = Field(None, description="Description Here")

    class Config:
        orm_mode = True


class SessionCreate(BaseModel):
    klass: Klass
    room: Room
    subject: Subject
    teacher: Teacher
    scheduled_start_time: datetime
    scheduled_end_time: datetime
    scenarios: Optional[List[SessionScenario]] = Field(None, description="List of scenarios")
    configs: Optional[List[SessionConfiguration]] = Field(None, description="List of configurations")

    class Config:
        orm_mode = True


class SessionUpdate(BaseModel):
    room: Optional[Room] = Field(None, description="Description Here")
    teacher: Optional[Teacher] = Field(None, description="Description Here")
    scheduled_start_time: Optional[datetime]
    scheduled_end_time: Optional[datetime]
    state: Optional[SessionState] = Field(None, description="Description Here")


class Session(SessionCreate):
    session_id: Optional[str] = Field(None, description="Description Here")
    actual_start_time: Optional[datetime] = Field(None, description="Description Here")
    actual_end_time: Optional[datetime] = Field(None, description="Description Here")
    video_url: Optional[List[str]] = Field(None, description="Description Here")

    class Config:
        orm_mode = True


class SessionIntervention(BaseModel):
    pass

