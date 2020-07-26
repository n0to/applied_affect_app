from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from app.models.enum_models import Scenario, Subject, Grade, Section, SessionState
from app.schemas.school import Klass as Klass
from app.schemas.teacher import Teacher
import bson

class SessionConfiguration(BaseModel):
    th_min_student_for_int: Optional[int] = Field(None, description="Description Here")
    th_min_gap_bet_int: Optional[int] = Field(None, description="Description Here")
    th_min_gap_for_student_int: Optional[int] = Field(None, description="Description Here")
    timestamp: Optional[datetime] = Field(None, description="Description Here")

    class Config:
        orm_mode = True


class SessionScenario(BaseModel):
    name: Optional[Scenario] = Field(None, title="State scenario")
    timestamp: Optional[datetime] = Field(None, description="Description Here")

    class Config:
        orm_mode = True


class SessionCreate(BaseModel):
    klass: Klass
    #room: str
    subject: str
    teacher: Teacher
    scheduled_start_time: datetime
    scheduled_end_time: datetime
    scenarios: Optional[List[SessionScenario]] = Field(None, description="List of scenarios")
    configs: Optional[List[SessionConfiguration]] = Field(None, description="List of configurations")


class SessionUpdate(BaseModel):
    room: Optional[str] = Field(None, description="Description Here")
    teacher_id: Optional[str] = Field(None, description="Description Here")
    scheduled_start_time: Optional[datetime]
    scheduled_end_time: Optional[datetime]
    state: Optional[SessionState] = Field(None, description="Description Here")


class Session(SessionCreate):
    _id: Any
    actual_start_time: Optional[datetime] = Field(None, description="Description Here")
    actual_end_time: Optional[datetime] = Field(None, description="Description Here")
    state: Optional[SessionState] = Field(None, description="Description Here")
    video_url: Optional[List[str]] = Field(None, description="Description Here")

    class Config:
        orm_mode = True


class SessionIntervention(BaseModel):
    pass

