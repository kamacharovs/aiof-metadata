import unittest
import math
import json

from aiof.car.core import loan_calc


class CarTestCase(unittest.TestCase):
    """Car unit tests"""

    def test_car_loan_calc_defaults(self):
        self.asset_loan_calc(
            loan_calc(
                car_loan=None,
                interest=None,
                years=None))

    def test_car_loan_calc_35(self):
        self.asset_loan_calc(
            loan_calc(
                car_loan=35000,
                interest=4,
                years=6))

    def asset_loan_calc(self, df):
        assert df is not None
        assert df.size > 0
        assert df.loc[len(df) - 1, "endingBalance"] == 0

        for index in range(1, len(df)):
            assert df.loc[index, "year"] > 0
            assert df.loc[index, "payments"] > 0
            assert df.loc[index, "principalPaid"] > 0
            assert df.loc[index, "interestPaid"] > 0
            assert df.loc[index, "startingBalance"] > 0
            assert df.loc[index, "endingBalance"] >= 0