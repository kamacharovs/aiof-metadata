import unittest
import json
import math

from aiof.retirement.core import *
from aiof.data.retirement import CommonInvestmentsRequest, NumberSimpleRequest, NumberRequest


class RetirementTestCase(unittest.TestCase):
    """
    Retirement unit tests
    """
    common_investments_req = CommonInvestmentsRequest(
        interest                        = 8,
        startYear                       = 2025,
        endYear                         = 2050,
        compoundingPeriods              = 12,
        fourOhOneKStartingAmount        = 15677,
        fourOhOneKMonthlyContributions  = 1625,
        rothIraStartingAmount           = 75489,
        rothIraMonthlyContributions     = 500,
        brokerageStartingAmount         = 9587,
        brokerageMonthlyContributions   = 250)

    number_simple_req = NumberSimpleRequest(
        currentSalary   = 40000)

    number_req = NumberRequest(
        desiredRetirementAge    = 60,
        desiredMonthlyIncome    = 6000,
        retirementEndAge        = 90)


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
            interest                            = self.common_investments_req.interest,
            start_year                          = self.common_investments_req.startYear,
            end_year                            = self.common_investments_req.endYear,
            compouding_periods                  = self.common_investments_req.compoundingPeriods,
            fourohone_k_starting_amount         = self.common_investments_req.fourOhOneKStartingAmount,
            fourohone_k_monthly_contributions   = self.common_investments_req.fourOhOneKMonthlyContributions,
            roth_ira_starting_amount            = self.common_investments_req.rothIraStartingAmount,
            roth_ira_monthly_contributions      = self.common_investments_req.rothIraMonthlyContributions,
            brokerage_starting_amount           = self.common_investments_req.brokerageStartingAmount,
            brokerage_monthly_contributions     = self.common_investments_req.brokerageMonthlyContributions))

    def test_common_investments_general_defaults(self):
        self.assert_common_investments(common_investments(
            interest                            = None,
            start_year                          = None,
            end_year                            = None,
            compouding_periods                  = None,
            fourohone_k_starting_amount         = self.common_investments_req.fourOhOneKStartingAmount,
            fourohone_k_monthly_contributions   = self.common_investments_req.fourOhOneKMonthlyContributions,
            roth_ira_starting_amount            = self.common_investments_req.rothIraStartingAmount,
            roth_ira_monthly_contributions      = self.common_investments_req.rothIraMonthlyContributions,
            brokerage_starting_amount           = self.common_investments_req.brokerageStartingAmount,
            brokerage_monthly_contributions     = self.common_investments_req.brokerageMonthlyContributions))

    def test_common_investments_fourohonek_defaults(self):
        self.assert_common_investments(common_investments(
            interest                            = self.common_investments_req.interest,
            start_year                          = self.common_investments_req.startYear,
            end_year                            = self.common_investments_req.endYear,
            compouding_periods                  = self.common_investments_req.compoundingPeriods,
            fourohone_k_starting_amount         = None,
            fourohone_k_monthly_contributions   = None,
            roth_ira_starting_amount            = self.common_investments_req.rothIraStartingAmount,
            roth_ira_monthly_contributions      = self.common_investments_req.rothIraMonthlyContributions,
            brokerage_starting_amount           = self.common_investments_req.brokerageStartingAmount,
            brokerage_monthly_contributions     = self.common_investments_req.brokerageMonthlyContributions))

    def test_common_investments_rothira_defaults(self):
        self.assert_common_investments(common_investments(
            interest                            = self.common_investments_req.interest,
            start_year                          = self.common_investments_req.startYear,
            end_year                            = self.common_investments_req.endYear,
            compouding_periods                  = self.common_investments_req.compoundingPeriods,
            fourohone_k_starting_amount         = self.common_investments_req.fourOhOneKStartingAmount,
            fourohone_k_monthly_contributions   = self.common_investments_req.fourOhOneKMonthlyContributions,
            roth_ira_starting_amount            = None,
            roth_ira_monthly_contributions      = None,
            brokerage_starting_amount           = self.common_investments_req.brokerageStartingAmount,
            brokerage_monthly_contributions     = self.common_investments_req.brokerageMonthlyContributions))

    def test_common_investments_brokerage_defaults(self):
        self.assert_common_investments(common_investments(
            interest                            = self.common_investments_req.interest,
            start_year                          = self.common_investments_req.startYear,
            end_year                            = self.common_investments_req.endYear,
            compouding_periods                  = self.common_investments_req.compoundingPeriods,
            fourohone_k_starting_amount         = self.common_investments_req.fourOhOneKStartingAmount,
            fourohone_k_monthly_contributions   = self.common_investments_req.fourOhOneKMonthlyContributions,
            roth_ira_starting_amount            = self.common_investments_req.rothIraStartingAmount,
            roth_ira_monthly_contributions      = self.common_investments_req.rothIraMonthlyContributions,
            brokerage_starting_amount           = None,
            brokerage_monthly_contributions     = None))

    def test_common_investments_interest_negative_raises_valueerror(self):
        with self.assertRaises(ValueError): 
            common_investments(
                interest                            = -self.common_investments_req.interest,
                start_year                          = self.common_investments_req.startYear,
                end_year                            = self.common_investments_req.endYear,
                compouding_periods                  = self.common_investments_req.compoundingPeriods,
                fourohone_k_starting_amount         = self.common_investments_req.fourOhOneKStartingAmount,
                fourohone_k_monthly_contributions   = self.common_investments_req.fourOhOneKMonthlyContributions,
                roth_ira_starting_amount            = self.common_investments_req.rothIraStartingAmount,
                roth_ira_monthly_contributions      = self.common_investments_req.rothIraMonthlyContributions,
                brokerage_starting_amount           = self.common_investments_req.brokerageStartingAmount,
                brokerage_monthly_contributions     = self.common_investments_req.brokerageMonthlyContributions)

    def test_common_investments_interest_toobig_raises_valueerror(self):
        with self.assertRaises(ValueError): 
            common_investments(
                interest                            = self.common_investments_req.interest * 1000,
                start_year                          = self.common_investments_req.startYear,
                end_year                            = self.common_investments_req.endYear,
                compouding_periods                  = self.common_investments_req.compoundingPeriods,
                fourohone_k_starting_amount         = self.common_investments_req.fourOhOneKStartingAmount,
                fourohone_k_monthly_contributions   = self.common_investments_req.fourOhOneKMonthlyContributions,
                roth_ira_starting_amount            = self.common_investments_req.rothIraStartingAmount,
                roth_ira_monthly_contributions      = self.common_investments_req.rothIraMonthlyContributions,
                brokerage_starting_amount           = self.common_investments_req.brokerageStartingAmount,
                brokerage_monthly_contributions     = self.common_investments_req.brokerageMonthlyContributions)

    def test_common_investments_endyear_less_than_startyear_raises_valueerror(self):
        with self.assertRaises(ValueError): 
            common_investments(
                interest                            = self.common_investments_req.interest,
                start_year                          = 2020,
                end_year                            = 2019,
                compouding_periods                  = self.common_investments_req.compoundingPeriods,
                fourohone_k_starting_amount         = self.common_investments_req.fourOhOneKStartingAmount,
                fourohone_k_monthly_contributions   = self.common_investments_req.fourOhOneKMonthlyContributions,
                roth_ira_starting_amount            = self.common_investments_req.rothIraStartingAmount,
                roth_ira_monthly_contributions      = self.common_investments_req.rothIraMonthlyContributions,
                brokerage_starting_amount           = self.common_investments_req.brokerageStartingAmount,
                brokerage_monthly_contributions     = self.common_investments_req.brokerageMonthlyContributions)

    def test_common_investments_fourohone_k_starting_amount_negative_raises_valueerror(self):
        with self.assertRaises(ValueError): 
            common_investments(
                interest                            = self.common_investments_req.interest,
                start_year                          = self.common_investments_req.startYear,
                end_year                            = self.common_investments_req.endYear,
                compouding_periods                  = self.common_investments_req.compoundingPeriods,
                fourohone_k_starting_amount         = -self.common_investments_req.fourOhOneKStartingAmount,
                fourohone_k_monthly_contributions   = self.common_investments_req.fourOhOneKMonthlyContributions,
                roth_ira_starting_amount            = self.common_investments_req.rothIraStartingAmount,
                roth_ira_monthly_contributions      = self.common_investments_req.rothIraMonthlyContributions,
                brokerage_starting_amount           = self.common_investments_req.brokerageStartingAmount,
                brokerage_monthly_contributions     = self.common_investments_req.brokerageMonthlyContributions)

    def test_common_investments_fourohone_k_monthly_contributions_negative_raises_valueerror(self):
        with self.assertRaises(ValueError): 
            common_investments(
                interest                            = self.common_investments_req.interest,
                start_year                          = self.common_investments_req.startYear,
                end_year                            = self.common_investments_req.endYear,
                compouding_periods                  = self.common_investments_req.compoundingPeriods,
                fourohone_k_starting_amount         = self.common_investments_req.fourOhOneKStartingAmount,
                fourohone_k_monthly_contributions   = -self.common_investments_req.fourOhOneKMonthlyContributions,
                roth_ira_starting_amount            = self.common_investments_req.rothIraStartingAmount,
                roth_ira_monthly_contributions      = self.common_investments_req.rothIraMonthlyContributions,
                brokerage_starting_amount           = self.common_investments_req.brokerageStartingAmount,
                brokerage_monthly_contributions     = self.common_investments_req.brokerageMonthlyContributions)

    def test_common_investments_roth_ira_starting_amount_negative_raises_valueerror(self):
        with self.assertRaises(ValueError): 
            common_investments(
                interest                            = self.common_investments_req.interest,
                start_year                          = self.common_investments_req.startYear,
                end_year                            = self.common_investments_req.endYear,
                compouding_periods                  = self.common_investments_req.compoundingPeriods,
                fourohone_k_starting_amount         = self.common_investments_req.fourOhOneKStartingAmount,
                fourohone_k_monthly_contributions   = self.common_investments_req.fourOhOneKMonthlyContributions,
                roth_ira_starting_amount            = -self.common_investments_req.rothIraStartingAmount,
                roth_ira_monthly_contributions      = self.common_investments_req.rothIraMonthlyContributions,
                brokerage_starting_amount           = self.common_investments_req.brokerageStartingAmount,
                brokerage_monthly_contributions     = self.common_investments_req.brokerageMonthlyContributions)

    def test_common_investments_roth_ira_monthly_contributions_negative_raises_valueerror(self):
        with self.assertRaises(ValueError): 
            common_investments(
                interest                            = self.common_investments_req.interest,
                start_year                          = self.common_investments_req.startYear,
                end_year                            = self.common_investments_req.endYear,
                compouding_periods                  = self.common_investments_req.compoundingPeriods,
                fourohone_k_starting_amount         = self.common_investments_req.fourOhOneKStartingAmount,
                fourohone_k_monthly_contributions   = self.common_investments_req.fourOhOneKMonthlyContributions,
                roth_ira_starting_amount            = self.common_investments_req.rothIraStartingAmount,
                roth_ira_monthly_contributions      = -self.common_investments_req.rothIraMonthlyContributions,
                brokerage_starting_amount           = self.common_investments_req.brokerageStartingAmount,
                brokerage_monthly_contributions     = self.common_investments_req.brokerageMonthlyContributions)

    def test_common_investments_brokerage_starting_amount_negative_raises_valueerror(self):
        with self.assertRaises(ValueError): 
            common_investments(
                interest                            = self.common_investments_req.interest,
                start_year                          = self.common_investments_req.startYear,
                end_year                            = self.common_investments_req.endYear,
                compouding_periods                  = self.common_investments_req.compoundingPeriods,
                fourohone_k_starting_amount         = self.common_investments_req.fourOhOneKStartingAmount,
                fourohone_k_monthly_contributions   = self.common_investments_req.fourOhOneKMonthlyContributions,
                roth_ira_starting_amount            = self.common_investments_req.rothIraStartingAmount,
                roth_ira_monthly_contributions      = self.common_investments_req.rothIraMonthlyContributions,
                brokerage_starting_amount           = -self.common_investments_req.brokerageStartingAmount,
                brokerage_monthly_contributions     = self.common_investments_req.brokerageMonthlyContributions)

    def test_common_investments_brokerage_monthly_contributions_negative_raises_valueerror(self):
        with self.assertRaises(ValueError): 
            common_investments(
                interest                            = self.common_investments_req.interest,
                start_year                          = self.common_investments_req.startYear,
                end_year                            = self.common_investments_req.endYear,
                compouding_periods                  = self.common_investments_req.compoundingPeriods,
                fourohone_k_starting_amount         = self.common_investments_req.fourOhOneKStartingAmount,
                fourohone_k_monthly_contributions   = self.common_investments_req.fourOhOneKMonthlyContributions,
                roth_ira_starting_amount            = self.common_investments_req.rothIraStartingAmount,
                roth_ira_monthly_contributions      = self.common_investments_req.rothIraMonthlyContributions,
                brokerage_starting_amount           = self.common_investments_req.brokerageStartingAmount,
                brokerage_monthly_contributions     = -self.common_investments_req.brokerageMonthlyContributions)

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


    def test_number_simple_defaults(self):
        res = number_simple(current_salary = self.number_simple_req.currentSalary)
        self.assert_number(res)

    def test_number_simple_random_salary(self):
        res = number_simple(current_salary = 125000)
        self.assert_number(res)

    def test_number_simple_negative_raises_valueerror(self):
        with self.assertRaises(ValueError): 
            number_simple(current_salary = -10)

    def test_number_defaults(self):
        res = number(
            desired_retirement_age  =   self.number_req.desiredRetirementAge,
            desired_monthly_income  =   self.number_req.desiredMonthlyIncome,
            retirement_end_age      =   self.number_req.retirementEndAge)
        self.assert_number(res)

    def test_number_random(self):
        res = number(
            desired_retirement_age  =   40,
            desired_monthly_income  =   8000,
            retirement_end_age      =   90)
        self.assert_number(res)

    def test_number_negative_desired_retirement_age_raises_valueerror(self):
        with self.assertRaises(ValueError): 
            number(
                desired_retirement_age  =   self.number_req.desiredRetirementAge * -1,
                desired_monthly_income  =   self.number_req.desiredMonthlyIncome,
                retirement_end_age      =   self.number_req.retirementEndAge)
    def test_number_zero_desired_retirement_age_raises_valueerror(self):
        with self.assertRaises(ValueError): 
            number(
                desired_retirement_age  =   self.number_req.desiredRetirementAge * 0,
                desired_monthly_income  =   self.number_req.desiredMonthlyIncome,
                retirement_end_age      =   self.number_req.retirementEndAge)

    def test_number_negative_desired_monthly_income_raises_valueerror(self):
        with self.assertRaises(ValueError): 
            number(
                desired_retirement_age  =   self.number_req.desiredRetirementAge,
                desired_monthly_income  =   self.number_req.desiredMonthlyIncome * -1,
                retirement_end_age      =   self.number_req.retirementEndAge)

    def test_number_negative_retirement_end_age_raises_valueerror(self):
        with self.assertRaises(ValueError): 
            number(
                desired_retirement_age  =   self.number_req.desiredRetirementAge,
                desired_monthly_income  =   self.number_req.desiredMonthlyIncome,
                retirement_end_age      =   self.number_req.retirementEndAge * -1)
    def test_number_zero_retirement_end_age_raises_valueerror(self):
        with self.assertRaises(ValueError): 
            number(
                desired_retirement_age  =   self.number_req.desiredRetirementAge,
                desired_monthly_income  =   self.number_req.desiredMonthlyIncome,
                retirement_end_age      =   self.number_req.retirementEndAge * 0)

    def assert_number(self, number):
        assert number is not None
        assert number > 0