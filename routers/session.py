from fastapi import APIRouter

router = APIRouter()


@router.get("/session/{id")
def get_session():
    pass


@router.put("/session/{id}")
def update_session():
    pass


@router.post("/session")
def create_session():
    pass


@router.get("/session/{id}/attendance")
def get_session_attendance():
    pass


@router.get("/session/{id}/pulse")
def get_session_pulse():
    pass


@router.get("/session/{id}/student_pulse")
def get_session_student_pulse():
    pass
