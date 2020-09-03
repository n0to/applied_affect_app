import pprint
import unittest

from fastapi.testclient import TestClient
from loguru import logger

from app.main import app

client = TestClient(app)
pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)


class TestMongo(unittest.TestCase):

    def test_sample(self):
        response = client.get("/info")
        logger.debug("This is sparta")
        pp.pprint(response.__dict__)

    def test_camera(self):
        response = client.get("/camera/5f32686b9c6348c3225aaab6")
        pp.pprint(response.__dict__)
