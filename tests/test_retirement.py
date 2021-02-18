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

    def test_withdrawal_calc_valid(self):
        self.assert_withdrawal_calc(withdrawal_calc(
            retirement_number   = 1500000,
            take_out_percentage = 7,
            number_of_years     = 35))

    def test_withdrawal_calc_valid_2(self):
        self.assert_withdrawal_calc(withdrawal_calc(
            retirement_number   = 3000000,
            take_out_percentage = 3.5,
            number_of_years     = 40))

    def test_withdrawal_calc_retirement_number_0(self):
        with self.assertRaises(ValueError): 
            withdrawal_calc(
                retirement_number   = 0,
                take_out_percentage = 3.5,
                number_of_years     = 30)

    def test_withdrawal_calc_retirement_number_negative(self):
        with self.assertRaises(ValueError): 
            withdrawal_calc(
                retirement_number   = -1000000,
                take_out_percentage = 3.5,
                number_of_years     = 30)

    def test_withdrawal_calc_take_out_percentage_0(self):
        with self.assertRaises(ValueError): 
            withdrawal_calc(
                retirement_number   = 1000000,
                take_out_percentage = 0,
                number_of_years     = 30)

    def test_withdrawal_calc_take_out_percentage_bigger_than_100(self):
        with self.assertRaises(ValueError): 
            withdrawal_calc(
                retirement_number   = 1000000,
                take_out_percentage = 101,
                number_of_years     = 30)

    def test_withdrawal_calc_take_out_percentage_negative(self):
        with self.assertRaises(ValueError): 
            withdrawal_calc(
                retirement_number   = 1000000,
                take_out_percentage = -3.5,
                number_of_years     = 30)

    def test_withdrawal_calc_take_out_percentage_100(self):
        with self.assertRaises(ValueError): 
            withdrawal_calc(
                retirement_number   = 1000000,
                take_out_percentage = 100,
                number_of_years     = 30)

    def test_withdrawal_calc_number_of_years_0(self):
        with self.assertRaises(ValueError): 
            withdrawal_calc(
                retirement_number   = 1000000,
                take_out_percentage = 3.5,
                number_of_years     = 0)

    def test_withdrawal_calc_number_of_years_bigger_than_100(self):
        with self.assertRaises(ValueError): 
            withdrawal_calc(
                retirement_number   = 1000000,
                take_out_percentage = 3.5,
                number_of_years     = 101)

    def test_withdrawal_calc_number_of_years_negative(self):
        with self.assertRaises(ValueError): 
            withdrawal_calc(
                retirement_number   = 1000000,
                take_out_percentage = 3.5,
                number_of_years     = -30)

    def assert_withdrawal_calc(self, df):
        assert df is not None
        assert df.size > 0

        for i in range (0, len(df)):
            assert df.loc[i, "year"] >= 1
            assert df.loc[i, "takeOutPercentage"] > 0
            assert df.loc[i, "startingRetirementNumber"] > 0
            assert df.loc[i, "withdrawal"] > 0
            assert df.loc[i, "endingRetirementNumber"] > 0


    def test_common_investments_defaults(self):
        self.assert_common_investments(common_investments(
            interest                            = None,
            start_year                          = None,
            end_year                            = None,
            compouding_periods                  = None,
            fourohone_k_starting_amount         = None,
            fourohone_k_monthly_contributions   = None,
            roth_ira_starting_amount            = None,
            roth_ira_monthly_contributions      = None,
            brokerage_starting_amount           = None,
            brokerage_monthly_contributions     = None))
    
    def test_common_investments_valid(self):
        self.assert_common_investments(common_investments(
            interest                            = 8,
            start_year                          = 2025,
            end_year                            = 2050,
            compouding_periods                  = 12,
            fourohone_k_starting_amount         = 15677,
            fourohone_k_monthly_contributions   = 1625,
            roth_ira_starting_amount            = 75489,
            roth_ira_monthly_contributions      = 500,
            brokerage_starting_amount           = 9587,
            brokerage_monthly_contributions     = 250))

    def test_common_investments_general_defaults(self):
        self.assert_common_investments(common_investments(
            interest                            = None,
            start_year                          = None,
            end_year                            = None,
            compouding_periods                  = None,
            fourohone_k_starting_amount         = 15677,
            fourohone_k_monthly_contributions   = 1625,
            roth_ira_starting_amount            = 75489,
            roth_ira_monthly_contributions      = 500,
            brokerage_starting_amount           = 9587,
            brokerage_monthly_contributions     = 250))

    def test_common_investments_fourohonek_defaults(self):
        self.assert_common_investments(common_investments(
            interest                            = 7,
            start_year                          = 2025,
            end_year                            = 2050,
            compouding_periods                  = 12,
            fourohone_k_starting_amount         = None,
            fourohone_k_monthly_contributions   = None,
            roth_ira_starting_amount            = 75489,
            roth_ira_monthly_contributions      = 500,
            brokerage_starting_amount           = 9587,
            brokerage_monthly_contributions     = 250))

    def test_common_investments_rothira_defaults(self):
        self.assert_common_investments(common_investments(
            interest                            = 7,
            start_year                          = 2025,
            end_year                            = 2050,
            compouding_periods                  = 12,
            fourohone_k_starting_amount         = 8957,
            fourohone_k_monthly_contributions   = 1625,
            roth_ira_starting_amount            = None,
            roth_ira_monthly_contributions      = None,
            brokerage_starting_amount           = 9587,
            brokerage_monthly_contributions     = 250))

    def test_common_investments_brokerage_defaults(self):
        self.assert_common_investments(common_investments(
            interest                            = 8,
            start_year                          = 2025,
            end_year                            = 2050,
            compouding_periods                  = 12,
            fourohone_k_starting_amount         = 15677,
            fourohone_k_monthly_contributions   = 1625,
            roth_ira_starting_amount            = 75489,
            roth_ira_monthly_contributions      = 500,
            brokerage_starting_amount           = None,
            brokerage_monthly_contributions     = None))

    def assert_common_investments(self, df):
        assert df is not None
        assert df.size > 0

        for i in range (0, len(df)):
            assert df.loc[i, "year"] >= 1
            assert df.loc[i, "compoundingPeriods"] >= 0
            assert df.loc[i, "fourohoneK"] >= 0
            assert df.loc[i, "fourohoneKMonthlyContributions"] >= 0
            assert df.loc[i, "rothIra"] >= 0
            assert df.loc[i, "rothIraMonthlyContributions"] >= 0
            assert df.loc[i, "brokerage"] >= 0
            assert df.loc[i, "brokerageMonthlyContributions"] >= 0
            assert df.loc[i, "total"] >= 0
            assert df.loc[i, "totalMonthlyContributions"] >= 0
