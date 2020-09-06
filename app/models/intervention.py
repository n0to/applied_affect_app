from datetime import datetime
from mongoengine import (
    Document,
    LazyReferenceField,
    BooleanField,
    IntField,
    DateTimeField,
    StringField, ReferenceField)
from app.models.session import Session
from app.models.student import Student


class SessionIntervention(Document):
    session = LazyReferenceField(Session)
    student_group_name = StringField()
    intervention_reason = StringField() # engagement, attention etc.
    intervention_period_start = DateTimeField()
    intervention_period_end = DateTimeField()
    intervention_reason_value = IntField()
    intervention_reason_threshold = IntField()
    datetime_modified = DateTimeField(default=datetime.now())
    datetime_sequence = DateTimeField(default=datetime.now())
    version = StringField()


class SessionInterventionStudent(Document):
    session = LazyReferenceField(Session)
    student = LazyReferenceField(Student)
    intervention_reason = StringField() # engagement, attention etc.
    intervention_period_start = DateTimeField()
    intervention_period_end = DateTimeField()
    intervention_reason_value = IntField()
    intervention_reason_threshold = IntField()
    datetime_modified = DateTimeField(default=datetime.now())
    datetime_sequence = DateTimeField(default=datetime.now())
    version = StringField()