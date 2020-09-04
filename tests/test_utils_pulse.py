import unittest
from datetime import datetime

from bson import ObjectId

from app.db.database import DbMgr
import pprint
from app.config import get_settings
import app.utils.pulse as utils_pulse
import bson
import app.models.pulse as models_pulse
import app.schemas.pulse_events as schemas_pulse_events
import app.models.session as models_session
import app.models.pulse_events as models_pulse_events
import app.utils.pulse_events as utils_pulse_events
import time
import random

pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)
session_id = '5f32686f9c6348c3225aaaea'
from fastapi import logger


class TestMongo(unittest.TestCase):
    @classmethod
    def setUp(cls):
        settings = get_settings()
        DbMgr.connect(settings.mongo_dbname,
                      settings.mongo_username,
                      settings.mongo_password,
                      settings.mongo_host)

    @classmethod
    def tearDown(cls):
        DbMgr.disconnect()

    def test_connection(self):
        pp.pprint("Established the connection and tested it")

    def test_session_raw(self):
        sess = models_session.Session.objects.get(id=session_id)
        pp.pprint(sess.id.generation_time)

    def test_get_session_attendance_aggregated(self):
        sat = utils_pulse.get_session_attendance_aggregated(session_id)
        pp.pprint(sat.dict())

    def test_session_pulse(self):
        pulse = utils_pulse.get_session_pulse(session_id)
        pp.pprint(pulse)

    def test_session_pulse_student(self):
        pulse = utils_pulse.get_session_pulse_student(session_id)
        pp.pprint(pulse)

    def test_foo(self):
        pulse_itr = models_pulse.SessionPulse.objects(session=session_id)
        for pulse in pulse_itr:
            pp.pprint(pulse.student_group.id)

    def test_bar(self):
        pp.pprint("")
        start = time.time()
        pulse_itr = models_pulse.SessionPulseStudent.objects(session=session_id)
        elapsed = time.time() - start
        pp.pprint("Elapsed: {}".format(elapsed))
        start = time.time()
        pp.pprint(len(pulse_itr))
        pp.pprint(pulse_itr[0])
        for pulse in pulse_itr:
            pp.pprint(str(pulse.student.id))
        elapsed = time.time() - start
        pp.pprint("Elapsed: {}".format(elapsed))

    def test_pulse_events(self):
        session_id = "5f427f3d293d7b69b5716d1f"
        camera_id = "5f427f37293d7b69b5716cf1"
        frame_type = "END"
        frame_number = 3
        person_id = "foobar" + str(random.randint(10, 12))
        image_url = "http://foobar.com"

        #sample = models_pulse_events.PulseProcessing(frame_type=frame_type,
        #                                             frame_number=frame_number,
        #                                             person_id=person_id,
        #                                             image_url=image_url,
        #                                             session=ObjectId(session_id),
        #                                             camera=ObjectId(camera_id))
        # sample.save()
        # person_detection_event: Optional[PersonDetectionEvent] = None
        # face_detection_event: Optional[FaceDetectionEvent] = None
        # face_embedding_event: Optional[FaceEmbeddingEvent] = None
        # face_recognition_event: Optional[FaceRecognitionEvent] = None
        # gaze_detection_event: Optional[GazeDetectionEvent] = None
        # action_recognition_event: Optional[ActionRecognitionEvent] = None
        gde = schemas_pulse_events.GazeDetectionEvent(roll=10, pitch=20, yaw=30, detected_at=datetime.now())
        are = schemas_pulse_events.ActionRecognitionEvent(
            actions=[schemas_pulse_events.Action(name="reading", confidence=0.5)],
            detected_at=datetime.now())

        fe = schemas_pulse_events.FaceEmbeddingEvent(embedding=[1,2,3], detected_at=datetime.now())
        #pp = schemas_pulse_events.PulseProcessing(frame_type=frame_type,
        #                                          frame_number=frame_number,
        #                                          person_id=person_id,
        #                                          image_url=image_url,
        #                                          gaze_detection_event=gde,
        #                                          action_recognition_event=are)
        pp = schemas_pulse_events.PulseProcessing(frame_type=frame_type,
                                                  frame_number=frame_number,
                                                  person_id=person_id,
                                                  image_url=image_url,
                                                  face_embedding_event=fe)
        event = utils_pulse_events.upsert_pulse_event(event=pp, session_id=session_id, camera_id=camera_id)
        print(event)
