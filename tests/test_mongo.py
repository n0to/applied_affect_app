import unittest
from app.db.database import DbMgr
import pprint
from app.models.session import Session as ModelSession
from app.models.user import User as ModelUser
from app.models.student import Guardian as ModelGuardian
from app.models.teacher import Teacher as ModelTeacher
from app.schemas.session import Session as SchemaSession
from app.config import get_settings


pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)


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
        session_id = '5f182bd52cd7d726a7155f91'
        sess = ModelSession.objects.get(id=session_id)
        pp.pprint(dict(sess.to_mongo()))
        pp.pprint(sess.klass.grade)
        pp.pprint(sess.room.name)
        pp.pprint("********************************************************")
        sout = SchemaSession.from_orm(sess)
        sout.session_id = str(sess.id)
        pp.pprint(sout.dict())

        #session = get_session(session_id=session_id)
        #pp.pprint(dict(session.to_mongo()))
        #pp.pprint(str(session.id))
        #pp.pprint(str(session.teacher.fetch().name))

    def test_get_user(self):
        email = "kevinmiles@example.com"
        usr = ModelGuardian.objects.get(email=email)
        pp.pprint(usr.name)

