from fastapi import APIRouter
import app.utils.pulse as pulse_utils
from app.schemas.pulse import SessionAttendanceAggregated

router = APIRouter()


@router.get("/session/{id}/attendance_aggregated", response_model=SessionAttendanceAggregated)
def get_session_attendance_aggregated(id: str):
    session_attendance_aggregated = pulse_utils.get_session_attendance_aggregated(id)
    return session_attendance_aggregated


@router.get("/session/{id}/pulse")
def get_session_pulse(id: str):
    pass


@router.get("/session/{id}/student_pulse")
def get_session_student_pulse(id: str):
    pass