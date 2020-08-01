import unittest
from app.config import get_settings
import pprint
pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)


class ConfigTestCase(unittest.TestCase):

    def test_config_prod(self):
        sett = get_settings()
        pp.pprint(sett.__dict__)



