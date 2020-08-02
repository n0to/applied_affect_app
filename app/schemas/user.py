from pydantic import BaseModel
from typing import Optional, List


class User(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    images: List[str] = []

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str
