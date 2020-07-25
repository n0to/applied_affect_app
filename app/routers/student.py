from fastapi import APIRouter

router = APIRouter()


@router.get("/student/")
def get_all_students():
    pass


@router.get("/student/{id}")
def get_student():
    pass


@router.put("/student/{id}")
def update_student():
    pass


@router.post("/student/{id}")
def create_student():
    pass


@router.get("/student/{id}/attendance")
def get_student_attendance():
    pass


@router.get("/student/{id}/pulse")
def get_student_pulse():
    pass


@router.get("/student/{id}/session/{s_id}/pulse")
def get_student_pulse():
    pass


@router.put("/guardian/{id}")
def update_guardian():
    pass


@router.get("/guardian/{id}/students")
def get_guardian_student():
    pass

