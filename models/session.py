import datetime

from mongoengine import EmbeddedDocument, DateTimeField, FloatField, IntField, StringField, Document, \
    LazyReferenceField, ListField, EmbeddedDocumentField, BooleanField, ReferenceField

from models.school import Room, Klass
from models.user import Student, StudentGroup, Teacher


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


class SessionAttendance(Document):
    session = LazyReferenceField(Session)
    student = LazyReferenceField(Student)
    is_present = BooleanField()


class SessionPulse(Document):
    session = LazyReferenceField(Session)
    attentiveness = IntField()
    engagement = IntField()
    student_group = LazyReferenceField(StudentGroup)


class SessionPulseStudent(Document):
    session = LazyReferenceField(Session)
    attentiveness = IntField()
    engagement = IntField()
    student = LazyReferenceField(Student)


class BoundingBox(EmbeddedDocument):
    x = FloatField(required=True)
    y = FloatField(required=True)
    length = FloatField(required=True)
    width = FloatField(required=True)


class FacialAnalysis(EmbeddedDocument):
    face_bbox = EmbeddedDocumentField(BoundingBox)
    roll = FloatField()
    pitch = FloatField()
    yaw = FloatField()


class SessionPulseStudentRaw(Document):
    frame_id = IntField(required=True)
    timestamp = DateTimeField(required=True)
    session = LazyReferenceField(Session, required=True)
    human_bbox = EmbeddedDocumentField(BoundingBox)
    facial_analysis = EmbeddedDocumentField(FacialAnalysis)
    detected_student = ReferenceField(Student)
    activity = StringField()


class SessionIntervention(Document):
    pass
