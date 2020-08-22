from fastapi import APIRouter
from fastapi.logger import logger
from typing import List
from app.schemas.pulse import SessionAttendanceAggregated, SessionPulse, SessionPulseStudent
import app.utils.pulse as pulse_utils

router = APIRouter()


@router.get("/session/{id}/attendance_aggregated", response_model=SessionAttendanceAggregated)
def get_session_attendance_aggregated(id: str):
    session_attendance_aggregated = pulse_utils.get_session_attendance_aggregated(id)
    return session_attendance_aggregated


@router.get("/session/{id}/pulse", response_model=List[SessionPulse])
def get_session_pulse(id: str):
    return pulse_utils.get_session_pulse(id)


@router.get("/session/{id}/student_pulse", response_model=List[SessionPulseStudent])
def get_session_student_pulse(id: str):
    return pulse_utils.get_session_pulse_student(id)