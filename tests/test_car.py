import unittest
import json

from aiof.car.core import *


class CarTestCase(unittest.TestCase):
    """Car unit tests"""

    def test_car_loan_calc_30_months(self):
        req = {
            "principalAmount": 25000,
            "numberOfMonths": 30,
            "rateOfInterest": 3.11
        }
        assert loan_calc(req) > 800
    def test_car_loan_calc_12_months(self):
        req = {
            "principalAmount": 25000,
            "numberOfMonths": 12,
            "rateOfInterest": 3.11
        }
        assert loan_calc(req) > 1600
    def test_car_loan_calc_1_month(self):
        req = {
            "principalAmount": 25000,
            "numberOfMonths": 1,
            "rateOfInterest": 3.11
        }
        assert loan_calc(req) > 25000