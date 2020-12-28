import unittest
import json
import math

from aiof.retirement.core import *


class RetirementTestCase(unittest.TestCase):
    """
    Retirement unit tests
    """

    def test_withdrawal_calc_defaults(self):
        self.assert_withdrawal_calc(withdrawal_calc(
            retirement_number   = None,
            take_out_percentage = None,
            number_of_years     = None))

    def assert_withdrawal_calc(self, df):
        assert df is not None
        assert df.size > 0

        for i in range (0, len(df)):
            assert df.loc[i, "year"] >= 1
            assert df.loc[i, "takeOutPercentage"] > 0
            assert df.loc[i, "startingRetirementNumber"] > 0
            assert df.loc[i, "withdrawal"] > 0
            assert df.loc[i, "endingRetirementNumber"] > 0
