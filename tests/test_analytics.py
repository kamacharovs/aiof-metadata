import unittest

from aiof.data.asset import Asset
from aiof.data.liability import Liability
from aiof.analytics.core import assets_fv, debt_to_income_ratio_calc, debt_to_income_ratio_basic_calc


class AnalyticsTestCase(unittest.TestCase):
    """Analytics unit tests"""

    test_assets = [
        Asset(name="asset 1",
            type="cash",
            value=35000),
        Asset(name="asset 2",
            type="cash",
            value=8000),
        Asset(name="asset 3",
            type="stock",
            value=24999)
    ]
    test_liabilities = [
        Liability(name="l 1",
            type="personal loan",
            value=1685.50,
            years=5,
            monthlyPayment=35),
        Liability(name="l 2",
            type="student loan",
            value=25000,
            years=10,
            monthlyPayment=208),
        Liability(name="l 3",
            type="car loan",
            value=34000,
            years=6,
            monthlyPayment=500)
    ]

    def test_assets_fv(self):
        assets_fv_res = assets_fv(assets=self.test_assets)
        
        assert len(assets_fv_res) > 0
        assert assets_fv_res[0].year > 0
        assert assets_fv_res[0].type == "cash" or "stock"
        assert assets_fv_res[0].interest > 0
        assert assets_fv_res[0].pv == self.test_assets[0].value
        assert assets_fv_res[0].fv > self.test_assets[0].value


    def test_debt_to_income_ratio_calc_liabilities(self):
        resp = debt_to_income_ratio_calc(income=150000, liabilities=self.test_liabilities)
        assert resp > 0

    def test_debt_to_income_ratio_calc_liabilities_is_zero(self):
        specific_liabilities = [
            Liability(name="l1",
                type="rv",
                value=1000)
        ]
        resp = debt_to_income_ratio_calc(income=150000, liabilities=specific_liabilities)
        assert resp == 0


    def test_debt_to_income_ratio_calc(self):
        resp = debt_to_income_ratio_basic_calc(income=50000, total_monthly_debt_payments=1250)
        assert resp > 0
        assert resp * 100 > 0

    def test_debt_to_income_ratio_calc_basic(self):
        resp = debt_to_income_ratio_basic_calc(income=1000, total_monthly_debt_payments=10)
        assert round(resp) == 12