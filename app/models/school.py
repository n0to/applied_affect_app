from mongoengine import Document, StringField, ListField, LazyReferenceField, URLField, ReferenceField, EmailField

from app.models.student import StudentGroup


class School(Document):
    name = StringField(required=True)
    group_name = StringField()
    location = StringField()
    email = EmailField()


class Camera(Document):
    name = StringField()
    stream_url = URLField(unique=True)
    position = StringField()


class Room(Document):
    cameras = ListField(ReferenceField(Camera))
    name = StringField(required=True, unique=True)


class Klass(Document):
    grade = StringField(required=True)
    section = StringField(required=True, unique_with='grade')
    student_groups = ListField(LazyReferenceField(StudentGroup))
    curriculum = StringField()
