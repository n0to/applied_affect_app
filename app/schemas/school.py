from pydantic import BaseModel, Field
from typing import List, Optional


class Klass(BaseModel):
    grade: str
    section: str
    curriculum: str

    class Config:
        orm_mode = True