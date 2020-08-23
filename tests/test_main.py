from fastapi.testclient import TestClient
from app.main import app
import pprint
import logging
import sys


pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)


def test_sample():
    response = client.get("/info")
    pp.pprint("This is sparta")
    pp.pprint(response.__dict__)


def test_camera():
    response = client.get("/camera/5f32686b9c6348c3225aaab6")
    pp.pprint(response.__dict__)


