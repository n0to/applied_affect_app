import datetime

from mongoengine import EmbeddedDocument, DateTimeField, FloatField, IntField, StringField, Document, \
    LazyReferenceField, ListField, EmbeddedDocumentField, URLField

from app.models.school import Room, Klass
from app.models.teacher import Teacher


class SessionConfiguration(EmbeddedDocument):
    timestamp = DateTimeField(default=datetime.datetime.now())
    # Minimum students in percentage to demonstrate some behavior to trigger class intervention
    th_min_student_for_int = FloatField(default=0.5)
    # Minimum time between two interventions. In seconds
    th_min_gap_bet_int = IntField(default=300)
    # Minimum time of observation before generating a student intervention. In seconds
    th_min_gap_for_student_int = IntField(default=180)


class SessionScenario(EmbeddedDocument):
    timestamp = DateTimeField(default=datetime.datetime.now())
    name = StringField(required=True)


class Session(Document):
    klass = LazyReferenceField(Klass, required=True)
    room = LazyReferenceField(Room, required=True)
    teacher = LazyReferenceField(Teacher, required=True)
    subject = StringField(required=True)
    scheduled_start_time = DateTimeField(required=True)
    scheduled_end_time = DateTimeField(required=True)
    actual_start_time = DateTimeField()
    actual_end_time = DateTimeField()
    scenarios = ListField(EmbeddedDocumentField(SessionScenario))
    configs = ListField(EmbeddedDocumentField(SessionConfiguration))
    video_url = ListField(URLField())


