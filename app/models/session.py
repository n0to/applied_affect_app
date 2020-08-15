import datetime

from mongoengine import EmbeddedDocument, DateTimeField, FloatField, IntField, StringField, Document, \
    LazyReferenceField, ListField, EmbeddedDocumentField, URLField, ReferenceField

from app.models.school import Room, Klass
from app.models.teacher import Teacher
from app.models.enums import SessionState, InterventionThresholdsDefaults


class SessionConfiguration(EmbeddedDocument):
    datetime_created = DateTimeField(default=datetime.datetime.now())
    # Minimum students in percentage to demonstrate some behavior to trigger class intervention
    th_min_student_for_int = IntField(default=InterventionThresholdsDefaults.MIN_STUDENT_FOR_INT)
    # Minimum time between two interventions. In seconds
    th_min_gap_bet_int = IntField(default=InterventionThresholdsDefaults.MIN_GAP_BET_INT)
    # Minimum time of observation before generating a student intervention. In seconds
    th_min_gap_for_student_int = IntField(default=InterventionThresholdsDefaults.MIN_GAP_BET_STUDENT_INT)


class SessionScenario(EmbeddedDocument):
    datetime_created = DateTimeField(default=datetime.datetime.now())
    name = StringField(required=True)


class Session(Document):
    klass = ReferenceField(Klass, required=True)
    room = ReferenceField(Room, required=True)
    teacher = ReferenceField(Teacher, required=True)
    subject = StringField(required=True)
    scheduled_start_time = DateTimeField(required=True)
    scheduled_end_time = DateTimeField(required=True)
    actual_start_time = DateTimeField()
    actual_end_time = DateTimeField()
    scenarios = ListField(EmbeddedDocumentField(SessionScenario))
    configs = ListField(EmbeddedDocumentField(SessionConfiguration))
    video_url = ListField(URLField())
    state = StringField(default=SessionState.Scheduled)
    datetime_modified = DateTimeField(default=datetime.datetime.now)


