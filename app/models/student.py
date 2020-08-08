from mongoengine import Document, StringField, ListField, URLField, BooleanField, ReferenceField, LazyReferenceField

from app.models.user import User


class Student(User):
    student_id = StringField(max_length=10)
    grade = StringField()
    curriculum = StringField()
    is_opt_out_individual = BooleanField(default=False)
    is_opt_out_aggregate = BooleanField(default=False)


class Guardian(User):
    students = ListField(ReferenceField(Student))


class StudentGroup(Document):
    name = StringField(required=True)
    members = ListField(ReferenceField(Student))
