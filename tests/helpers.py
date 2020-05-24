import unittest
import json

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
        assert compound_interest_calc(1000, 5, 8) > 1000

    def test_compound_interest_all_frequencies(self):
        frequencies = [
            "daily",
            "monthly",
            "quarterly",
            "half-year",
            "yearly"
        ]
        for f in frequencies:
            assert compound_interest_calc(1000, 5, 8) > 1000


    
    def test_loan_payments_calc_monthly(self):
        assert loan_payments_calc(10000, 5, 7) > 0
    def test_loan_payments_calc_yearly(self):
        assert loan_payments_calc(10000, 5, 7, "yearly") > 0
    def test_loan_payments_calc_monthly_exact(self):
        assert loan_payments_calc(200000, 15, 7.5) == 1854.0247200054619

    def test_loan_payments_calc_as_table_yearly(self):
        loan_json = json.loads(loan_payments_calc_as_table(10000, 6, 7, "yearly"))
        loan_json_len = len(loan_json)

        assert loan_json[0]["year"] == 1
        assert loan_json[loan_json_len - 1]["year"] == 6

    def test_loan_payments_calc_as_table_monthly(self):
        loan_json = json.loads(loan_payments_calc_as_table(200000, 15, 7.5))
        loan_json_len = len(loan_json)
        
        assert loan_json[0]["month"] == 1
        assert loan_json[loan_json_len - 1]["month"] == 180



    def test_simple_interest_calc(self):
        assert simple_interest_calc(1000, 15, 5) == 7.5


    
    def test_equated_monthly_installment_calc(self):
        assert equated_monthly_installment_calc(1000, 7.5, 36) > 0


if __name__ == "__main__":
    unittest.main()