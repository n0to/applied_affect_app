from datetime import datetime

from mongoengine import (
    Document,
    StringField,
    ListField,
    BooleanField,
    ReferenceField,
    DateTimeField,
    EmbeddedDocument)

from app.models.user import User


class Student(User):
    school_id = StringField(max_length=10)
    grade = StringField()
    curriculum = StringField()
    is_opt_out_individual = BooleanField(default=False)
    is_opt_out_aggregate = BooleanField(default=False)


class Guardian(User):
    students = ListField(ReferenceField(Student))


class StudentGroup(EmbeddedDocument):
    name = StringField(required=True)
    members = ListField(ReferenceField(Student))
    datetime_modified = DateTimeField(default=datetime.now)
