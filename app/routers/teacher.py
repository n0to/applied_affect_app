from fastapi import APIRouter

router = APIRouter()


@router.get("/teacher/")
def get_all_teachers():
    pass


@router.get("/teacher/{id}")
def get_teacher():
    pass


@router.get("/teacher/{id}/session")
def get_teacher_session():
    pass


@router.get("/teacher/{id}/session/{s_id}/pulse")
def get_teacher_session_pulse():
    pass


@router.get("/teacher/{id}/pulse")
def get_teacher_pulse():
    pass


@router.post("/teacher/{id}/session")
def create_teacher_session():
    pass