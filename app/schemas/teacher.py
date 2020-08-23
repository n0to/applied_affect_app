from app.schemas.user import User


class Teacher(User):
    school_id: str

    class Config:
        orm_mode = True


class SchoolAdmin(User):
    school_id: str

    class Config:
        orm_mode = True
