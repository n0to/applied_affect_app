from pydantic import BaseModel, EmailStr, AnyHttpUrl, Field
from typing import Optional, List


class User(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    images: List[AnyHttpUrl] = []
    disabled: Optional[bool] = Field(False)
    role: str = Field(alias='_cls')

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str

    class Config:
        orm_mode = True
