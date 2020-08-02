from pydantic import BaseModel, Field
from typing import List, Optional

from app.schemas.user import User


class Teacher(User):
    teacher_id: str

    class Config:
        orm_mode = True
