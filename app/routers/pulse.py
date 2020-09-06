from datetime import datetime
from typing import List, Optional, Union

from fastapi import APIRouter, HTTPException

import app.utils.pulse as utils_pulse
from app.schemas.pulse import SessionAttendanceAggregated, SessionPulse, SessionPulseStudent, SessionPulseAggregated, \
    SessionAttendance, StudentIntervention, StudentGroupIntervention

router = APIRouter()


@router.get("/session/{id}/attendance", response_model=List[SessionAttendance])
def get_session_attendance_aggregated(id: str):
    session_attendance = utils_pulse.get_session_attendance(session_id=id)
    if not len(session_attendance):
        raise HTTPException(status_code=400, detail="No attendance found with given session id")
    return session_attendance


@router.get("/session/{id}/attendance_aggregated", response_model=SessionAttendanceAggregated)
def get_session_attendance_aggregated(id: str):
    session_attendance_aggregated = utils_pulse.get_session_attendance_aggregated(session_id=id)
    if not session_attendance_aggregated:
        raise HTTPException(status_code=400, detail="No attendance found with given session id")
    return session_attendance_aggregated


@router.get("/session/{id}/pulse", response_model=List[SessionPulse])
def get_session_pulse(id: str, from_datetime: Optional[datetime] = None, to_datetime: Optional[datetime] = None):
    session_pulse = utils_pulse.get_session_pulse(session_id=id, from_datetime=from_datetime, to_datetime=to_datetime)
    if not len(session_pulse):
        raise HTTPException(status_code=400, detail="No pulse found for given session")
    return session_pulse


@router.get("/session/{id}/pulse_aggregated", response_model=SessionPulseAggregated)
def get_session_pulse_aggregated(id: str, to_datetime: Optional[datetime] = None):
    session_pulse_aggregated = utils_pulse.get_session_pulse_aggregated(id, to_datetime)
    if not session_pulse_aggregated:
        raise HTTPException(status_code=400, detail="No attendance found with given session id")
    return session_pulse_aggregated


@router.get("/session/{id}/student_pulse", response_model=List[SessionPulseStudent])
def get_session_student_pulse(id: str):
    session_pulse_student = utils_pulse.get_session_pulse_student(session_id=id)
    if not len(session_pulse_student):
        raise HTTPException(status_code=400, detail="No pulse found for given session")
    return session_pulse_student


@router.get("/session/{id}/interventions", response_model=List[Union[StudentIntervention, StudentGroupIntervention]])
def get_session_interventions(id: str, from_datetime: Optional[datetime] = None, to_datetime: Optional[datetime] = None):
    session_interventions = utils_pulse.get_session_interventions(session_id=id, from_datetime=from_datetime, to_datetime=to_datetime)
    if not len(session_interventions):
        raise HTTPException(status_code=400, detail="No interventions found for given session")
    return session_interventions
