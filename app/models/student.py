from mongoengine import Document, StringField, ListField, URLField, BooleanField, ReferenceField, LazyReferenceField

from app.models.user import User


class Student(Document):
    student_id = StringField(required=True, unique=True)
    name = StringField()
    grade = StringField(required=True)
    curriculum = StringField(required=True)
    images = ListField(URLField())
    is_opt_out_individual = BooleanField(default=False)
    is_opt_out_aggregate = BooleanField(default=False)


class Guardian(User):
    students = ListField(ReferenceField(Student), required=True)


class StudentGroup(Document):
    name = StringField(required=True)
    members = ListField(LazyReferenceField(Student))