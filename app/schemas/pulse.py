from datetime import datetime

from pydantic import BaseModel


class SessionAttendanceAggregated(BaseModel):
    present: int
    unknown: int
    total: int


class SessionPulse(BaseModel):
    timestamp: datetime
    student_group_name: str
    attentiveness: int
    engagement: int