import unittest
import json
import math

from aiof.house.core import *


class HouseTestCase(unittest.TestCase):
    """House unit tests"""

    def test_mortgage_calc_defaults(self):
        self.mortgage_calc_assert(mortgage_calc())

    def test_mortgage_calc_15(self):
        self.mortgage_calc_assert(
            mortgage_calc(
                property_value      =   150000,
                down_payment        =   15000,
                interest_rate       =   2.75,
                loan_term_years     =   15,
                start_date          =   datetime.datetime.utcnow() + datetime.timedelta(days=10),
                pmi                 =   0.05,
                property_insurance  =   0,
                monthly_hoa         =   0
            )
        )

    def test_mortgage_calc_30(self):
        self.mortgage_calc_assert(
            mortgage_calc(
                property_value      =   250000,
                down_payment        =   50000,
                interest_rate       =   4.25,
                loan_term_years     =   30,
                start_date          =   datetime.datetime.utcnow() + datetime.timedelta(days=365),
                pmi                 =   0.05,
                property_insurance  =   0,
                monthly_hoa         =   0
            )
        )

    def test_mortgage_calc_invalid_loan_amount_raises_value_error(self):
        with self.assertRaises(ValueError): 
            mortgage_calc(
                property_value  = 150000,
                down_payment    = 200000)

    def test_mortgage_calc_invalid_down_payment_raises_value_error(self):
        with self.assertRaises(ValueError): 
            mortgage_calc(down_payment = -1)

    def test_mortgage_calc_invalid_loan_term_years_raises_value_error(self):
        with self.assertRaises(ValueError): 
            mortgage_calc(loan_term_years = -1)
        with self.assertRaises(ValueError): 
            mortgage_calc(loan_term_years = 150)

    def test_mortgage_calc_invalid_invalid_interest_rate_raises_value_error(self):
        with self.assertRaises(ValueError): 
            mortgage_calc(interest_rate = 101)
        with self.assertRaises(ValueError): 
            mortgage_calc(interest_rate = -1)

    def test_mortgage_calc_invalid_pmi_raises_value_error(self):
        with self.assertRaises(ValueError): 
            mortgage_calc(pmi = 101)
        with self.assertRaises(ValueError): 
            mortgage_calc(pmi = -1)

    def test_mortgage_calc_invalid_property_insurance_raises_value_error(self):
        with self.assertRaises(ValueError): 
            mortgage_calc(property_insurance = -1)

    def test_mortgage_calc_invalid_monthly_hoa_raises_value_error(self):
        with self.assertRaises(ValueError): 
            mortgage_calc(monthly_hoa = -1)
        
    def mortgage_calc_assert(self, df):
        assert df is not None
        assert df.size > 0
        assert df.loc[len(df), "endingBalance"] == 0

        for index in range(2, len(df) + 1):
            assert df.loc[index, "payment"] > 0
            assert df.loc[index, "principalPaid"] > 0
            assert df.loc[index, "interestPaid"] > 0
            assert df.loc[index, "startingBalance"] > 0
            assert df.loc[index, "endingBalance"] >= 0
            assert math.floor(round(df.loc[index, "payment"], 1)) == math.floor(round(df.loc[index, "principalPaid"] + df.loc[index, "interestPaid"], 1))


    def test_mortgage_calc_yearly(self):
        assert house_mortgage_calc(250000, 3.25, 30) > 0


    def test_house_future_value_calc(self):
        assert round(house_future_value_calc(1000, 2, 5), 2) == 5204.04


    def test_sample(self):
        loan_json = json.loads((house_sample()).to_json(orient="records"))
        loan_json_len = len(loan_json)

        assert loan_json[0]["year"] == 1
        assert loan_json[loan_json_len - 1]["year"] == 30
        assert loan_json[loan_json_len - 1]["endingBalance"] == 0