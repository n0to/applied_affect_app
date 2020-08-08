import unittest
from app.db.database import DbMgr
import pprint
from app.config import get_settings
import app.utils.pulse as utils_pulse
import bson
import app.models.pulse as models_pulse
import app.models.session as models_session

pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)
session_id = '5f269246a24cbc0b2f561d09'


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