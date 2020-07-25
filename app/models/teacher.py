from mongoengine import StringField

from app.models.user import User


class Teacher(User):
    teacher_id = StringField(required=True, unique=True)