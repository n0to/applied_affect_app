from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, AnyUrl


class PersonDetectionEvent(BaseModel):
    top_left_x: int
    top_left_y: int
    bottom_right_x: int
    bottom_right_y: int
    image_width: int
    image_height: int
    confidence: float
    object_label: str
    detected_at: datetime

    class Config:
        orm_mode = True


class FaceDetectionEvent(BaseModel):
    top_left_x: int
    top_left_y: int
    bottom_right_x: int
    bottom_right_y: int
    image_width: int
    image_height: int
    confidence: float
    object_label: str
    detected_at: datetime

    class Config:
        orm_mode = True


class FaceEmbeddingEvent(BaseModel):
    embedding: List[float]
    detected_at: datetime

    class Config:
        orm_mode = True


class FaceRecognitionEvent(BaseModel):
    face_id: str
    detected_at: datetime

    class Config:
        orm_mode = True


class GazeDetectionEvent(BaseModel):
    roll: float
    pitch: float
    yaw: float
    detected_at: datetime

    class Config:
        orm_mode = True


class Action(BaseModel):
    name: str
    confidence: float

    class Config:
        orm_mode = True


class ActionRecognitionEvent(BaseModel):
    actions: List[Action] = []
    detected_at: datetime

    class Config:
        orm_mode = True


class PulseProcessing(BaseModel):
    frame_type: str
    frame_number: int
    person_id: str
    image_url: AnyUrl
    person_detection_event: Optional[PersonDetectionEvent] = None
    face_detection_event: Optional[FaceDetectionEvent] = None
    face_embedding_event: Optional[FaceEmbeddingEvent] = None
    face_recognition_event: Optional[FaceRecognitionEvent] = None
    gaze_detection_event: Optional[GazeDetectionEvent] = None
    action_recognition_event: Optional[ActionRecognitionEvent] = None

    class Config:
        orm_mode = True
