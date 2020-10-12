import unittest

from aiof.data.asset import Asset
from aiof.analytics.core import assets_fv


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

    def test_assets_fv(self):
        assets_fv_res = assets_fv(assets=self.test_assets)
        
        assert len(assets_fv_res) > 0
        assert assets_fv_res[0].year > 0
        assert assets_fv_res[0].type == "cash" or "stock"
        assert assets_fv_res[0].interest > 0
        assert assets_fv_res[0].pv == self.test_assets[0].value
        assert assets_fv_res[0].fv > self.test_assets[0].value