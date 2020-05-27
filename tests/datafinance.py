import unittest
import json
import pandas as pd

from aiof.data.asset import Asset
from aiof.data.liability import Liability
from aiof.data.goal import Goal
from aiof.data.finance import Finance


class FinanceTestCase(unittest.TestCase):
    """Finance unit tests"""


    def test_finance_total_assets_value(self):
        assets = [
            Asset("nissan versa", "car", 14500),
            Asset("house", "house", 250000)
        ]
        liabilities = [
            Liability("why did I spend money on this?", "credit card", 878),
            Liability("test", "mortgage", 150000)
        ]
        goals = [
            Goal("savings", "short-term")
        ]

        finance = Finance(assets, liabilities, goals)

        assert finance.get_total_assets_value() == 264500
        assert finance.get_distinct_assets_types() == ["car", "house"]
        assert finance.get_total_liabilities_value() == 150878
        assert finance.get_total_balance_sheet() > 0