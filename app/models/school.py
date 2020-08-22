from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    ListField,
    LazyReferenceField,
    URLField,
    ReferenceField,
    EmailField,
    DateTimeField)
from app.models.student import StudentGroup


class School(Document):
    name = StringField(required=True)
    group_name = StringField()
    location = StringField()
    email = EmailField()
    datetime_modified = DateTimeField(default=datetime.now())


class Camera(Document):
    name = StringField()
    stream_url = URLField(unique=True)
    position = StringField()
    datetime_modified = DateTimeField(default=datetime.now())


class Room(Document):
    cameras = ListField(ReferenceField(Camera))
    name = StringField(required=True, unique=True)
    datetime_modified = DateTimeField(default=datetime.now())


class Klass(Document):
    grade = StringField(required=True)
    section = StringField(required=True, unique_with='grade')
    student_groups = ListField(ReferenceField(StudentGroup))
    curriculum = StringField()
    datetime_modified = DateTimeField(default=datetime.now())
