import unittest
import math
import json

from aiof.car.core import loan_calc, value_depreciation_calc


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

    def asset_loan_calc(self, resp):
        assert resp.carLoan > 0
        assert resp.interest > 0
        assert resp.years > 0
        assert resp.monthlyPayment > 0
        assert resp.data is not None
        assert resp.data.size > 0
        assert resp.data.loc[len(resp.data) - 1, "endingBalance"] == 0

        for index in range(1, len(resp.data)):
            assert resp.data.loc[index, "year"] > 0
            assert resp.data.loc[index, "payments"] > 0
            assert resp.data.loc[index, "principalPaid"] > 0
            assert resp.data.loc[index, "interestPaid"] > 0
            assert resp.data.loc[index, "startingBalance"] > 0
            assert resp.data.loc[index, "endingBalance"] >= 0


    def test_value_depreciation_calc_defaults(self):
        self.assert_value_depreciation_calc(
            value_depreciation_calc(
                initial_value=None,
                years=None))

    def test_value_depreciation_calc_less_than_six_years_issuccessful(self):
        self.assert_value_depreciation_calc(
            value_depreciation_calc(
                initial_value=25000,
                years=4))

    def test_value_depreciation_calc_more_than_six_years_issuccessful(self):
        self.assert_value_depreciation_calc(
            value_depreciation_calc(
                initial_value=25000,
                years=7))

    def assert_value_depreciation_calc(self, df):
        assert df is not None
        assert df.size > 0

        for i in range(0, len(df)):
            assert df.iloc[i, 0] > 0
            assert df.iloc[i, 1] > 0
            assert df.iloc[i, 2] > 0
        for i in range(1, len(df)):
            assert df.iloc[i, 2] < df.iloc[i - 1, 2]