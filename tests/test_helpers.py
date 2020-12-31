import unittest
import json
import pandas as pd

from aiof.helpers import *


class HelpersTestCase(unittest.TestCase):
    """Helpers unit tests"""

    def test_convert_frequency_daily(self):
        assert convert_frequency("daily") == 365

    def test_convert_frequency_multiple_frequencies(self):
        frequencires = [
            "daily",
            "quarterly",
            "yearly"
        ]
        for f in frequencires:
            assert convert_frequency(f) > 0

    def test_convert_frequency_raises_exception(self):
        with self.assertRaises(Exception): convert_frequency("test")


    def test_to_percentage_80(self):
        assert to_percentage(80) == 0.8
    def test_to_percentage_5(self):
        assert to_percentage(5) == 0.05

    def test_to_percentage_raises_exception(self):
        with self.assertRaises(Exception): to_percentage(200)


    def test_compound_interest(self):
        assert compound_interest_calc(1000, 5, 8) > 0

    def test_compound_interest_all_frequencies(self):
        frequencies = [
            "daily",
            "monthly",
            "quarterly",
            "half-year",
            "yearly"
        ]
        for f in frequencies:
            assert compound_interest_calc(1000, 5, 8) > 0

    
    def test_loan_payments_calc_monthly(self):
        assert loan_payments_calc(10000, 5, 7) > 0
    def test_loan_payments_calc_yearly(self):
        assert loan_payments_calc(10000, 5, 7, "yearly") > 0
    def test_loan_payments_calc_monthly_exact(self):
        assert round(loan_payments_calc(200000, 15, 7.5), 2) == 1854.02
    def test_loan_payments_calc_monthly_30000(self):
        assert round(loan_payments_calc(30000, 6, 4.5), 2) == 476.22

    def test_loan_payments_calc_as_table_yearly(self):
        loan_json = json.loads((loan_payments_calc_as_table(10000, 6, 7, "yearly")).to_json(orient="records"))
        loan_json_len = len(loan_json)

        assert loan_json[0]["year"] == 1
        assert loan_json[loan_json_len - 1]["year"] == 6
        assert loan_json[loan_json_len - 1]["endingBalance"] == 0

    def test_loan_payments_calc_as_table_monthly(self):
        loan_json = json.loads((loan_payments_calc_as_table(30000, 6, 4.5)).to_json(orient="records"))
        loan_json_len = len(loan_json)
        
        assert loan_json[0]["month"] == 1
        assert loan_json[loan_json_len - 1]["month"] == 72
        assert loan_json[loan_json_len - 1]["endingBalance"] == 0

    def test_loan_payments_calc_as_table_monthly_as_df(self):
        payments_df = loan_payments_calc_as_table(30000, 6, 4.5)


    def test_simple_interest_calc(self):
        assert simple_interest_calc(1000, 15, 5) == 7.5

    
    def test_equated_monthly_installment_calc(self):
        assert equated_monthly_installment_calc(1000, 7.5, 36) > 0


    def test_doubling_time_with_continuous_compounding_6_percent(self):
        assert round(doubling_time_with_continuous_compounding(6), 2) == 11.55
    def test_doubling_time_with_continuous_compounding_10_percent(self):
        assert round(doubling_time_with_continuous_compounding(10), 2) == 6.93


    def test_fv(self):
        fv_res = fv(
            interest=5,
            years=5,
            pmt=0,
            pv=5000)
        assert round(fv_res, 2) == 6416.79
    def test_fv_with_pmt(self):
        fv_res = fv(
            interest=5,
            years=5,
            pmt=250,
            pv=5000)
        assert round(fv_res, 2) > 6416.79
    def test_fv_small_interest(self):
        fv_res = fv(
            interest=0.01,
            years=2,
            pmt=0,
            pv=5000)
        assert round(fv_res, 2) > 5000


    def test_get_current_month_first(self):
        datem = get_current_month_first()
        assert datem is not None
        assert datem.day == 1
        assert datem.month > 0
        assert datem.year > 0
