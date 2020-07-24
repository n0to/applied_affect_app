from fastapi import APIRouter
from ..schemas.session import *

router = APIRouter()


@router.get("/session/{id")
def get_session(id: str):
    pass


@router.put("/session/{id}")
def update_session(id: str):
    pass


@router.post("/session")
def create_session(session: SessionCreate):
    pass


@router.get("/session/{id}/attendance")
def get_session_attendance(id: str):
    pass


@router.get("/session/{id}/pulse")
def get_session_pulse(id: str):
    pass


@router.get("/session/{id}/student_pulse")
def get_session_student_pulse(id: str):
    pass
