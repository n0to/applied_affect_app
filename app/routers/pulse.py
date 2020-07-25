from fastapi import APIRouter

router = APIRouter()


@router.get("/session/{id}/attendance")
def get_session_attendance(id: str):
    pass


@router.get("/session/{id}/pulse")
def get_session_pulse(id: str):
    pass


@router.get("/session/{id}/student_pulse")
def get_session_student_pulse(id: str):
    pass