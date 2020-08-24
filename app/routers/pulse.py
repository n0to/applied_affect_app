from datetime import datetime
from fastapi import APIRouter, HTTPException
from loguru import logger
from typing import List, Optional
from app.schemas.pulse import SessionAttendanceAggregated, SessionPulse, SessionPulseStudent
import app.utils.pulse as pulse_utils

router = APIRouter()


@router.get("/session/{id}/attendance_aggregated", response_model=SessionAttendanceAggregated)
def get_session_attendance_aggregated(id: str):
    session_attendance_aggregated = pulse_utils.get_session_attendance_aggregated(id)
    if not session_attendance_aggregated:
        raise HTTPException(status_code=400, detail="No attendance found with given session id")
    return session_attendance_aggregated


@router.get("/session/{id}/pulse", response_model=List[SessionPulse])
def get_session_pulse(id: str, from_datetime: Optional[datetime] = None, to_datetime: Optional[datetime] = None):
    session_pulse = pulse_utils.get_session_pulse(id, from_datetime, to_datetime)
    if not len(session_pulse):
        raise HTTPException(status_code=400, detail="No pulse found for given session")
    return session_pulse


@router.get("/session/{id}/student_pulse", response_model=List[SessionPulseStudent])
def get_session_student_pulse(id: str):
    session_pulse_student = pulse_utils.get_session_pulse_student(id)
    if not len(session_pulse_student):
        raise HTTPException(status_code=400, detail="No pulse found for given session")
    return session_pulse_student
