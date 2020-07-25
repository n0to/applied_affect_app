from mongoengine import Document, LazyReferenceField, BooleanField, IntField, EmbeddedDocument, FloatField, \
    EmbeddedDocumentField, DateTimeField, ReferenceField, StringField

from app.models.session import Session
from app.models.student import Student, StudentGroup


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