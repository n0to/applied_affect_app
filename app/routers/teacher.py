from fastapi import APIRouter
from loguru import logger
from typing import List
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
    return utils_teacher.get_teacher(id)


@router.get("/teacher/{id}/sessions", response_model=List[Session])
def get_teacher_session(id: str):
    logger.debug("Getting sessions for teacher id: {}".format(id))
    return utils_teacher.get_teacher_sessions(id)


@router.get("/teacher/{id}/session/{s_id}/pulse", response_model=List[SessionPulse])
def get_teacher_session_pulse(id: str, s_id: str):
    pass


@router.get("/teacher/{id}/pulse", response_model=List[SessionPulseAggregated])
def get_teacher_pulse(id: str):
    pass


@router.post("/teacher/{id}/session", response_model=str)
def create_teacher_session():
    pass