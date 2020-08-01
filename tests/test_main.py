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
logging.getLogger('faker').setLevel(logging.ERROR)
client = TestClient(app)
logging.getLogger('faker').setLevel(logging.ERROR)


def test_sample():
    response = client.get("/info")
    pp.pprint("This is sparta")
    pp.pprint(response.__dict__)

