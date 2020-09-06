from datetime import datetime
from mongoengine import (
    Document,
    LazyReferenceField,
    BooleanField,
    IntField,
    DateTimeField,
    StringField, ReferenceField, DecimalField)
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
    attentiveness = DecimalField()
    engagement = DecimalField()
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
    datetime_sequence = DateTimeField(default=datetime.now())
    version = StringField()
    intervention_reason = StringField()  # engagement, attention etc.
    intervention_period_start = DateTimeField()
    intervention_period_end = DateTimeField()
    intervention_reason_value = DecimalField()
    intervention_reason_threshold = DecimalField()
    meta = {'allow_inheritance': True}


class StudentGroupIntervention(SessionIntervention):
    student_group_name = StringField()


class StudentIntervention(SessionIntervention):
    student = ReferenceField(Student)


