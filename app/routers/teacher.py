from typing import List

from fastapi import APIRouter

from app.schemas.pulse import SessionPulse, SessionPulseAggregated
from app.schemas.session import Session
from app.schemas.teacher import Teacher

router = APIRouter()


@router.get("/teacher/", response_model=List[Teacher])
def get_all_teachers():
    pass


@router.get("/teacher/{id}", response_model=Teacher)
def get_teacher():
    pass


@router.get("/teacher/{id}/session", response_model=List[Session])
def get_teacher_session():
    pass


@router.get("/teacher/{id}/session/{s_id}/pulse", response_model=List[SessionPulse])
def get_teacher_session_pulse():
    pass


@router.get("/teacher/{id}/pulse", response_model=List[SessionPulseAggregated])
def get_teacher_pulse():
    pass


@router.post("/teacher/{id}/session", response_model=str)
def create_teacher_session():
    pass