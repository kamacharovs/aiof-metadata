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
        for c in coast_fire_savings_resp:
            assert c.total is not None
            assert c.initialEarning is not None
            assert c.withdrawFour is not None
            assert c.withdrawThree is not None
            assert c.withdrawTwo is not None
            assert c.presentValueFour is not None
            assert c.presentValueThree is not None
            assert c.withdrawTwo is not None