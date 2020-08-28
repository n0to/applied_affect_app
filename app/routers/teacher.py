from datetime import datetime

from fastapi import APIRouter, HTTPException
from loguru import logger
from typing import List, Optional

from pydantic import PositiveInt

from app.models.enums import SessionState, Grade, Section, Subject
from app.schemas.pulse import SessionPulse, SessionPulseAggregated
from app.schemas.session import Session, SessionList
from app.schemas.teacher import Teacher
import app.utils.teacher as utils_teacher
import app.utils.session as utils_session

router = APIRouter()


@router.get("/teacher/{id}", response_model=Teacher)
def get_teacher(id: str):
    teacher = utils_teacher.get_teacher(id=id)
    if not teacher:
        raise HTTPException(status_code=400, detail="No such teacher exists")
    return teacher


@router.get("/teacher/{id}/sessions", response_model=List[Session])
def get_sessions(id: str,
                 state: Optional[SessionState] = None,
                 grade: Optional[Grade] = None,
                 section: Optional[Section] = None,
                 subject: Optional[Subject] = None,
                 scheduled_end_time: Optional[datetime] = None,
                 scheduled_start_time: Optional[datetime] = datetime.now(),
                 max_records: Optional[PositiveInt] = 3):
    sessions = utils_session.search_sessions(state=state,
                                             scheduled_start_time=scheduled_start_time,
                                             scheduled_end_time=scheduled_end_time,
                                             max_records=max_records,
                                             grade=grade,
                                             section=section,
                                             subject=subject,
                                             teacher=id)
    if not len(sessions):
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions


@router.get("/teacher/{id}/session/{s_id}/pulse", response_model=List[SessionPulseAggregated])
def get_teacher_session_pulse(id: str, s_id: str):
    pass


@router.get("/teacher/{id}/pulse", response_model=SessionPulseAggregated)
def get_teacher_pulse(id: str):
    pass
