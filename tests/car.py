import unittest
import json

from aiof.car.core import *


class CarTestCase(unittest.TestCase):
    """Car unit tests"""

    def test_car_loan_calc_30_months(self):
        assert loan_calc(25000, 3.11, 30) > 800
    def test_car_loan_calc_12_months(self):
        assert loan_calc(25000, 3.11, 12) > 1600
    def test_car_loan_calc_1_month(self):
        assert loan_calc(25000, 3.11, 1) > 25000