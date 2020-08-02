import unittest
from app.config import get_settings
import pprint
import os
pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)


class ConfigTestCase(unittest.TestCase):

    def test_config_prod(self):
        sett = get_settings()
        pp.pprint(os.path.dirname(os.path.realpath(__file__)))
        pp.pprint(sett.__dict__)



