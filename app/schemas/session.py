from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.enums import Scenario, Subject, SessionState
from app.schemas.mongo_helpers import ObjectIdStr
from app.schemas.school import Klass, Room, KlassWithoutStudentList
from app.schemas.teacher import Teacher


class SessionConfiguration(BaseModel):
    th_min_student_for_int: Optional[int] = Field(None)
    th_min_gap_bet_int: Optional[int] = Field(None)
    th_min_gap_for_student_int: Optional[int] = Field(None)
    datetime_created: Optional[datetime] = Field(None, description="Description Here")

    class Config:
        orm_mode = True


class SessionScenario(BaseModel):
    name: Scenario = Field(None)
    datetime_created: Optional[datetime] = Field(None, description="Description Here")

    class Config:
        orm_mode = True


class SessionCreate(BaseModel):
    klass: KlassWithoutStudentList
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
    scheduled_start_time: Optional[datetime] = Field(None)
    scheduled_end_time: Optional[datetime] = Field(None)
    state: Optional[SessionState] = Field(None, description="Description Here")
    scenarios: Optional[SessionScenario] = Field(None, description="Description Here")
    configs: Optional[SessionConfiguration] = Field(None, description="Description Here")

    class Config:
        orm_mode = True


class Session(SessionCreate):
    actual_start_time: Optional[datetime] = Field(None, description="Description Here")
    actual_end_time: Optional[datetime] = Field(None, description="Description Here")
    video_url: Optional[List[str]] = Field(None, description="Description Here")
    id: ObjectIdStr

    class Config:
        orm_mode = True
