import unittest
from app.db.database import DbMgr
import pprint
from app.config import get_settings
import app.utils.session as utils_session
import app.models.session as models_session
import app.schemas.session as schemas_session

pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)
session_id = '5f269246a24cbc0b2f561d09'
teacher_id = '5f32686f9c6348c3225aaae0'


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
        sessions = models_session.Session.objects(teacher=teacher_id).order_by('+scheduled_start_time').limit(3)
        out_sessions = []
        for session in sessions:
            pp.pprint(str(session.id))
            out_sessions.append(schemas_session.Session.from_orm(session))

        for session in out_sessions:
            pp.pprint(session.dict())

