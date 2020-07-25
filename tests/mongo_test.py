import unittest
from app.db.database import DbMgr
import sys
import logging
from app.crud.session import *
import pprint

logger = logging.getLogger()
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)


class TestMongo(unittest.TestCase):
    @classmethod
    def setUp(cls):
        DbMgr.connect()

    @classmethod
    def tearDown(cls):
        DbMgr.disconnect()

    def testConnection(self):
        logger.debug("Established the connection and tested it")

    def test_get_session(self):
        session_id = '5f182bd52cd7d726a7155f91'
        session = get_session(session_id=session_id)
        pp.pprint(dict(session.to_mongo()))
        pp.pprint(str(session.id))
        pp.pprint(str(session.teacher.fetch().name))
