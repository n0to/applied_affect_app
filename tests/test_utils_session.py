import unittest
from app.db.database import DbMgr
import pprint
from app.config import get_settings
import app.utils.session as utils_session
import app.models.session as models_session
import app.models.school as models_school
import app.schemas.school as schemas_school
import app.models.pulse as models_pulse
from pydantic.utils import GetterDict
from mongoengine.base.datastructures import LazyReference
from datetime import datetime

from app.models.enums import Subject, Grade, SessionState, Section

pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)
session_id = '5f425a3e1a6cff03a067141c'


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

    def test_get_session(self):
        sess = utils_session.get_session(session_id)
        pp.pprint(sess.dict())

    def test_update_session(self):
        sess = models_session.Session.objects.get(id=session_id)
        pp.pprint(type(sess.room))
        pp.pprint(sess.room.id)

    def test_camera(self):
        camera = models_school.Camera.objects.first()
        pp.pprint(camera.to_mongo())
        foo = GetterDict(camera)
        pp.pprint(foo.keys())
        pp.pprint(foo['id'])
        out_cam = schemas_school.Camera.from_orm(camera)
        pp.pprint(out_cam.dict())
        pp.pprint(out_cam.to_json())

    def test_room(self):
        room = models_school.Room.objects.first()
        pp.pprint(room.to_mongo())

    def test_session_student_pulse(self):
        pulseitr = models_pulse.SessionPulseStudent.objects(session=session_id)
        for pulse in pulseitr:
            if isinstance(pulse.student, LazyReference) is True:
                pp.pprint("BLAAAH")

    def test_search_sessions_with_klass(self):
        max_records = 5
        state = SessionState.Scheduled.name
        grade = Grade.Sixth
        section = Section.B
        subject = Subject.Chemistry
        teacher = "5f427f3c293d7b69b5716d1a"
        klass = models_school.Klass.objects(grade=grade, section=section).first()
        pp.pprint(str(klass.id))
        # scheduled_start_time = datetime.strptime("", "%Y%m%d %H:%M:%S")
        # scheduled_end_time = datetime.strptime("", "%Y%m%d %H:%M:%S")
        #sessions = utils_session.search_sessions(max_records=max_records,
        #                                         state=state,
        #                                         # scheduled_start_time=scheduled_start_time,
        #                                         # scheduled_end_time=scheduled_end_time,
        #                                         klass=str(klass.id),
        #                                         subject=subject,
        #                                         teacher=teacher)

    def test_search_sessions(self):
        max_records = 50
        state = SessionState.Scheduled.name
        teacher = "5f427f3c293d7b69b5716d1a"
        #scheduled_start_time = datetime.strptime("20200826 08:00:00", "%Y%m%d %H:%M:%S")
        scheduled_start_time = datetime.now()
        scheduled_end_time = datetime.strptime("20200831 08:00:00", "%Y%m%d %H:%M:%S")
        sessions = utils_session.search_sessions(max_records=max_records,
                                                 teacher=teacher,
                                                 state=state,
                                                 scheduled_start_time=scheduled_start_time,
                                                 scheduled_end_time=scheduled_end_time)
        for session in sessions:
            pp.pprint(session.scheduled_start_time)
