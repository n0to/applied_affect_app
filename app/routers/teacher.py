from datetime import datetime

from fastapi import APIRouter, HTTPException
from loguru import logger
from typing import List, Optional
from app.schemas.pulse import SessionPulse, SessionPulseAggregated
from app.schemas.session import Session
from app.schemas.teacher import Teacher
import app.utils.teacher as utils_teacher


router = APIRouter()


@router.get("/teacher/", response_model=List[Teacher])
def get_all_teachers():
    pass


@router.get("/teacher/{id}", response_model=Teacher)
def get_teacher(id: str):
    teacher = utils_teacher.get_teacher(id)
    if not teacher:
        raise HTTPException(status_code=400, detail="No such teacher exists")
    return teacher


@router.get("/teacher/{id}/sessions", response_model=List[Session])
def get_teacher_session(id: str, start_datetime: Optional[datetime], max_records=Optional[int]):
    sessions = utils_teacher.get_teacher_sessions(id=id, start_datetime=start_datetime, max_records=max_records)
    if not len(sessions):
        raise HTTPException(status_code=400, detail="No sessions for given teacher")
    return sessions


@router.get("/teacher/{id}/session/{s_id}/pulse", response_model=List[SessionPulse])
def get_teacher_session_pulse(id: str, s_id: str):
    pass


@router.get("/teacher/{id}/pulse", response_model=List[SessionPulseAggregated])
def get_teacher_pulse(id: str):
    pass


@router.post("/teacher/{id}/session", response_model=str)
def create_teacher_session():
    pass