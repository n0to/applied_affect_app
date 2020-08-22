import unittest
from app.db.database import DbMgr
import pprint
from app.config import get_settings
import app.utils.auth as utils_auth
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

    def test_verify_password(self):
        plain_password = "foobar"
        hashed_password = utils_auth.get_password_hash(plain_password)
        pp.pprint("Hashed Password: {}".format(hashed_password))


