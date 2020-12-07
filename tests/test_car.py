import unittest
import json

from aiof.car.core import loan_calc


class CarTestCase(unittest.TestCase):
    """Car unit tests"""

    def test_car_loan_calc_defaults(self):
        res = loan_calc(
            car_loan=None,
            interest=None,
            years=None)
        self.asset_loan_calc(res)

    def asset_loan_calc(self, res):
        assert res > 0