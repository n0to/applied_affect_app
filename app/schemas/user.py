from typing import Optional, List
from pydantic import BaseModel, EmailStr, AnyHttpUrl, Field
from app.schemas.mongo_helpers import ObjectIdStr


class User(BaseModel):
    id: ObjectIdStr
    name: str
    email: EmailStr
    phone: str
    images: List[AnyHttpUrl] = []
    disabled: Optional[bool] = Field(False)
    role: str = Field(alias='_cls')

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str

    class Config:
        orm_mode = True
