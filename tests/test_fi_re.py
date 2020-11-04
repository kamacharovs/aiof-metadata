import unittest
import datetime

from aiof.fi.re import *


class FireTestCase(unittest.TestCase):
    """Fire unit tests"""

    
    def test_fi_re_coast_fire_savings(self):
        coast_fire_savings_resp = coast_fire_savings()

        assert len(coast_fire_savings_resp) > 0
        assert coast_fire_savings_resp[0].age > 0
        assert coast_fire_savings_resp[0].year == datetime.datetime.now().year