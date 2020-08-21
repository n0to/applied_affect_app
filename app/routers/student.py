from typing import List

from fastapi import APIRouter

from app.schemas.student import Student, StudentAttendanceAggregated, StudentPulseAggregated, StudentSessionPulse

router = APIRouter()


@router.get("/student/", response_model=List[Student])
def get_all_students():
    pass


@router.get("/student/{id}", response_model=Student)
def get_student(id: str):
    pass


@router.put("/student/{id}")
def update_student():
    pass


@router.post("/student/{id}")
def create_student():
    pass


@router.get("/student/{id}/attendance", response_model=StudentAttendanceAggregated)
def get_student_attendance(id: str):
    pass


@router.get("/student/{id}/pulse", response_model=StudentPulseAggregated)
def get_student_pulse(id: str):
    pass


@router.get("/student/{id}/session/{s_id}/pulse", response_model=StudentSessionPulse)
def get_student_pulse(id: str, s_id: str):
    pass


@router.put("/guardian/{id}")
def update_guardian():
    pass


@router.get("/guardian/{id}/students", response_model=List[Student])
def get_guardian_student(id: str):
    pass

