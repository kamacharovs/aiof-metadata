import unittest

from aiof.data.asset import Asset
from aiof.data.liability import Liability
from aiof.analytics.core import analyze, assets_fv, debt_to_income_ratio_calc, debt_to_income_ratio_basic_calc, life_event_types, life_event_df_f


class AnalyticsTestCase(unittest.TestCase):
    """Analytics unit tests"""

    test_assets = [
        Asset(name="asset 1",
            typeName="cash",
            value=35000),
        Asset(name="asset 2",
            typeName="cash",
            value=8000),
        Asset(name="asset 3",
            typeName="stock",
            value=24999)
    ]
    test_liabilities = [
        Liability(name="l1",
            typeName="personal loan",
            value=1685.50,
            years=5,
            monthlyPayment=35),
        Liability(name="l2",
            typeName="student loan",
            value=25000,
            years=10,
            monthlyPayment=208),
        Liability(name="l3",
            typeName="car loan",
            value=34000,
            years=6,
            monthlyPayment=500)
    ]


    def test_analyze(self):
        resp = analyze(self.test_assets, self.test_liabilities, 150000)

        assert len(resp.assets) > 0
        assert len(resp.liabilities) > 0
        assert resp.assetsTotal > 0
        assert resp.assetsMean > 0
        assert resp.liabilitiesTotal > 0
        assert resp.liabilitiesMean > 0
        assert resp.analytics.diff > 0
        assert resp.analytics.cashToCcRatio > 0
        assert resp.analytics.debtToIncomeRatio > 0
        assert len(resp.analytics.assetsFv) > 0


    def test_assets_fv(self):
        resp = assets_fv(assets=self.test_assets)   

        assert len(resp) > 0
        assert resp[0].year > 0
        assert resp[0].typeName == "cash" or "stock"
        assert resp[0].interest > 0
        assert resp[0].pv == self.test_assets[0].value
        assert resp[0].fv > self.test_assets[0].value


    def test_debt_to_income_ratio_calc_liabilities(self):
        resp = debt_to_income_ratio_calc(150000, self.test_liabilities)

        assert resp > 0

    def test_debt_to_income_ratio_calc_liabilities_is_zero(self):
        specific_liabilities = [
            Liability(name="l1",
                typeName="rv",
                value=1000)
        ]
        resp = debt_to_income_ratio_calc(150000, specific_liabilities)

        assert resp == 0

    def test_debt_to_income_ratio_calc_no_monthly_payment_but_years(self):
        specific_liabilities = [
            Liability(name="l1",
                typeName="personal loan",
                value=5000,
                years=5),
            Liability(name="l2",
                typeName="auto lease",
                value=12500,
                years=6)
        ]
        resp = debt_to_income_ratio_calc(150000, specific_liabilities)

        assert resp > 0
        assert resp > 1


    def test_debt_to_income_ratio_basic_calc(self):
        resp = debt_to_income_ratio_basic_calc(50000, 1250)

        assert resp > 0

    def test_debt_to_income_ratio_basic_calc_exact(self):
        resp = debt_to_income_ratio_basic_calc(1000, 10)

        assert round(resp) == 12


    def test_life_event_types_issuccessful(self):
        types = life_event_types()

        assert types is not None
        assert len(types) > 0
        assert types[0] is not None
        assert types[0] != ""


    def test_life_event_df_f_issuccessful(self):
        df = life_event_df_f(
            asset_type="investment",
            years=25,
            start_amount=35000,
            monthly_contribution=750
        )

        assert df is not None
        assert df.iloc[0][0] > 0
        assert df.iloc[0][1] > 0
        assert df.iloc[0][2] > 0
        assert df.iloc[0][3] > 0