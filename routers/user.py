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


@router.post("/teacher/{id}/session")
def create_teacher_session():
    pass


@router.get("/student/")
def get_all_students():
    pass


@router.get("/student/{id}")
def get_student():
    pass


@router.put("/student/{id}")
def update_student():
    pass


@router.put("/guardian/{id}")
def update_guardian():
    pass


@router.get("/guardian/{id}/students")
def get_guardian_student():
    pass
