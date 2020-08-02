from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    email: Optional[str] = None


class UserInDB(User):
    hashed_password: str
