from mongoengine import StringField
from app.models.user import User


class Teacher(User):
    school_id = StringField(max_length=10)


class SchoolAdmin(User):
    school_id = StringField(max_length=10)
