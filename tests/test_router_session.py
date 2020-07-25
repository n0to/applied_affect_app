from fastapi.testclient import TestClient
from app.main import app
import pprint
import logging
import sys

logger = logging.getLogger()
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)
client = TestClient(app)


def test_get_session():
    pass


