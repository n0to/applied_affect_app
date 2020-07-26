from pydantic import BaseModel, Field
from typing import List, Optional


class TeacherCreate(BaseModel):
    teacher_id: str
    name: str
    email: str
    ref_image_urls: Optional[List[str]]


class Teacher(TeacherCreate):
    class Config:
        orm_mode = True
