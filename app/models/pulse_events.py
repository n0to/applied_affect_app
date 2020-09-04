from mongoengine import EmbeddedDocument, Document, StringField, IntField, URLField, EmbeddedDocumentField, FloatField, \
    DateTimeField, ListField, LazyReferenceField
from mongoengine.base import LazyReference

from app.models.school import Camera
from app.models.session import Session


class PersonDetectionEvent(EmbeddedDocument):
    top_left_x = IntField()
    top_left_y = IntField()
    bottom_right_x = IntField()
    bottom_right_y = IntField()
    image_width = IntField()
    image_height = IntField()
    confidence = FloatField()
    object_label = StringField()
    detected_at = DateTimeField()


class FaceDetectionEvent(EmbeddedDocument):
    top_left_x = IntField()
    top_left_y = IntField()
    bottom_right_x = IntField()
    bottom_right_y = IntField()
    image_width = IntField()
    image_height = IntField()
    confidence = FloatField()
    object_label = StringField()
    detected_at = DateTimeField()


class FaceEmbeddingEvent(EmbeddedDocument):
    embedding = ListField(FloatField)
    detected_at = DateTimeField()


class FaceRecognitionEvent(EmbeddedDocument):
    face_id = StringField()
    detected_at = DateTimeField()


class GazeDetectionEvent(EmbeddedDocument):
    roll = FloatField()
    pitch = FloatField()
    yaw = FloatField()
    detected_at = DateTimeField()


class Action(EmbeddedDocument):
    name = StringField()
    confidence = FloatField()


class ActionRecognitionEvent(EmbeddedDocument):
    actions = ListField(EmbeddedDocumentField(Action))
    detected_at = DateTimeField()


class PulseProcessing(Document):
    session = LazyReferenceField(Session)
    camera = LazyReferenceField(Camera)
    frame_type = StringField()
    frame_number = IntField()
    person_id = StringField(unique=True, required=True)  # is a hash of session, camera, frame_number by pipeline
    image_url = URLField()
    person_detection_event = EmbeddedDocumentField(PersonDetectionEvent)
    face_detection_event = EmbeddedDocumentField(FaceDetectionEvent)
    face_embedding_event = EmbeddedDocumentField(FaceEmbeddingEvent)
    face_recognition_event = EmbeddedDocumentField(FaceRecognitionEvent)
    gaze_detection_event = EmbeddedDocumentField(GazeDetectionEvent)
    action_recognition_event = EmbeddedDocumentField(ActionRecognitionEvent)