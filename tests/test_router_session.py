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
    response = client.get("/session/5f182bd52cd7d726a7155f91")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
    pp.pprint(response)


