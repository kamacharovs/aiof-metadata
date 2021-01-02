import unittest
import datetime

from aiof.fi.re import *
from aiof.data.fi import CoastFireSavings, CoastFireSavingsRequest


class FireTestCase(unittest.TestCase):
    """Fire unit tests"""

    test_savings = [
        CoastFireSavings(
            age=25,
            year=datetime.datetime.today().year,
            contribution=75000,
            yearlyReturn=0.08),
        CoastFireSavings(
            age=26,
            year=datetime.datetime.today().year + 1,
            contribution=75000,
            yearlyReturn=0.08),
        CoastFireSavings(
            age=27,
            year=datetime.datetime.today().year + 2,
            contribution=75000,
            yearlyReturn=0.08),
        CoastFireSavings(
            age=28,
            year=datetime.datetime.today().year + 3,
            contribution=0,
            yearlyReturn=0.06)
    ]
    test_savings_req = CoastFireSavingsRequest(
            savings=test_savings,
            initialInterestRate=0.02,
            currentBalance=150000)
    
    def test_fi_re_coast_fire_savings_defaults(self):
        coast_fire_savings_resp = coast_fire_savings(
            coast_savings=self.test_savings_req.savings,
            initial_interest_rate=self.test_savings_req.initialInterestRate,
            current_balance=self.test_savings_req.currentBalance)

        assert len(coast_fire_savings_resp) > 0
        assert coast_fire_savings_resp[0].age > 0
        assert coast_fire_savings_resp[0].year == datetime.datetime.today().year
        for c in coast_fire_savings_resp:
            assert c.total is not None
            assert c.initialEarning is not None
            assert c.withdrawFour is not None
            assert c.withdrawThree is not None
            assert c.withdrawTwo is not None
            assert c.presentValueFour is not None
            assert c.presentValueThree is not None
            assert c.withdrawTwo is not None
            