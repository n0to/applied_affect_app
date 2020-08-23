from datetime import datetime
from mongoengine import (
    Document,
    LazyReferenceField,
    BooleanField,
    IntField,
    DateTimeField,
    StringField)
from app.models.session import Session
from app.models.student import Student, StudentGroup


class SessionAttendance(Document):
    session = LazyReferenceField(Session)
    student = LazyReferenceField(Student)
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


'''
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
    datetime_modified = DateTimeField(default=datetime.datetime.now)
    session = LazyReferenceField(Session, required=True)
    human_bbox = EmbeddedDocumentField(BoundingBox)
    facial_analysis = EmbeddedDocumentField(FacialAnalysis)
    detected_student = ReferenceField(Student)
    activity = StringField()


class SessionIntervention(Document):
    pass
'''
