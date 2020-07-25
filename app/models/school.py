from mongoengine import Document, StringField, ListField, LazyReferenceField, URLField

from app.models.user import StudentGroup


class School(Document):
    name = StringField(required=True)
    group_name = StringField()
    location = StringField()
    email = StringField()


class Camera(Document):
    name = StringField()
    stream_url = URLField()
    position = StringField()


class Room(Document):
    cameras = ListField(LazyReferenceField(Camera))
    name = StringField(required=True, unique=True)


class Klass(Document):
    grade = StringField(required=True)
    section = StringField(required=True, unique_with='grade')
    student_groups = ListField(LazyReferenceField(StudentGroup))
    curriculum = StringField()