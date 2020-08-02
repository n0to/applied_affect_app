from pydantic import BaseModel
from typing import Optional, List

from app.schemas.user import User


class Student(User):
    pass


class Guardian(User):
    pass

