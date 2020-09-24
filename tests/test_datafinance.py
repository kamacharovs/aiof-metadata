import unittest
import json
import pandas as pd

from aiof.data.asset import Asset
from aiof.data.liability import Liability
from aiof.data.goal import Goal
from aiof.data.finance import Finance


class FinanceTestCase(unittest.TestCase):
    """Finance unit tests"""

    def get_test_finance(self):
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

        return Finance(1, assets, liabilities, goals)

    def test_finance_total_assets_value(self):
        finance = self.get_test_finance()

        assert finance.get_total_assets_value() == 264500
        assert finance.get_distinct_assets_types() == ["car", "house"]
        assert finance.get_total_liabilities_value() == 150878
        assert finance.get_distinct_liabilities_types() == ["credit card", "mortgage"]
        assert finance.get_total_balance_sheet() > 0

    def test_finance_total_stats(self):
        finance = self.get_test_finance()
        finance_stats = finance.get_total_finance_stats()
        
        assert finance_stats["assets"] > 0
        assert finance_stats["liabilities"] > 0
        assert finance_stats["balanceSheet"] > 0