from datetime import datetime
from mongoengine import (
    Document,
    LazyReferenceField,
    BooleanField,
    IntField,
    DateTimeField,
    StringField, ReferenceField)
from app.models.session import Session
from app.models.student import Student, StudentGroup


class SessionAttendance(Document):
    session = LazyReferenceField(Session)
    student = ReferenceField(Student)
    is_present = BooleanField()
    datetime_modified = DateTimeField(default=datetime.now())
    version = StringField()


class SessionPulse(Document):
    session = LazyReferenceField(Session)
    attentiveness = IntField()
    engagement = IntField()
    student_group_name = StringField()
    datetime_modified = DateTimeField(default=datetime.now())
    datetime_sequence = DateTimeField(default=datetime.now())
    version = StringField()


class SessionPulseStudent(Document):
    session = LazyReferenceField(Session)
    attentiveness = IntField()
    engagement = IntField()
    student = LazyReferenceField(Student)
    datetime_modified = DateTimeField(default=datetime.now())
    datetime_sequence = DateTimeField(default=datetime.now())
    version = StringField()


class SessionIntervention(Document):
    session = LazyReferenceField(Session)
    datetime_created = DateTimeField(default=datetime.now())

    meta = {'allow_inheritance': True}


class StudentGroupIntervention(SessionIntervention):
    name = StringField()


class StudentIntervention(SessionIntervention):
    student = ReferenceField(Student)


