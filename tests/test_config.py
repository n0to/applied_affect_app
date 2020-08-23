import unittest
from app.config import get_settings
import pprint
import os
import random
from datetime import datetime

pp = pprint.PrettyPrinter(indent=2, sort_dicts=True)


class ConfigTestCase(unittest.TestCase):

    def test_config_prod(self):
        sett = get_settings()
        pp.pprint(os.path.dirname(os.path.realpath(__file__)))
        pp.pprint(sett.__dict__)

    def test_date(self):
        hour = random.randint(8, 14)
        year = '2020'
        month = random.randint(8,8)
        day = random.randint(1,23)
        date_str = f'{year}{month:02}{day:02} {hour:02}:00:00'
        print(date_str)
        st_time = datetime.strptime(date_str, "%Y%m%d %H:%M:%S")
        pp.pprint(st_time)
        pp.pprint(datetime.now())
