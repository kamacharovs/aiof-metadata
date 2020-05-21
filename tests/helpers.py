import unittest
import json

from .context import aiof


class HelpersTestSuite(unittest.TestCase):
    """Helpers unit tests"""

    def test_convert_frequency_daily(self):
        assert aiof.convert_frequency("daily") == 365

    def test_convert_frequency_multiple_frequencies(self):
        frequencires = [
            "daily",
            "quarterly",
            "yearly"
        ]
        for f in frequencires:
            assert aiof.convert_frequency(f) > 0

    def test_convert_frequency_raises_exception(self):
        with self.assertRaises(Exception): aiof.convert_frequency("test")



    def test_to_percentage_80(self):
        assert aiof.to_percentage(80) == 0.8
    def test_to_percentage_5(self):
        assert aiof.to_percentage(5) == 0.05

    def test_to_percentage_raises_exception(self):
        with self.assertRaises(Exception): aiof.to_percentage(200)



    def test_compound_interest(self):
        assert aiof.compound_interest_calc(1000, 5, 8) > 1000

    def test_compound_interest_all_frequencies(self):
        frequencies = [
            "daily",
            "monthly",
            "quarterly",
            "half-year",
            "yearly"
        ]
        for f in frequencies:
            assert aiof.compound_interest_calc(1000, 5, 8) > 1000


    
    def test_loan_payments_calc_yearly(self):
        assert aiof.loan_payments_calc(10000, 5, 7) > 0
    def test_loan_payments_calc_monthly(self):
        assert aiof.loan_payments_calc(10000, 5, 7, "monthly") > 0

    def test_loan_payments_calc_as_table(self):
        loan_json = json.loads(aiof.loan_payments_calc_as_table(10000, 6, 7))
        loan_json_len = len(loan_json)

        assert loan_json[0]["year"] == 1
        assert loan_json[loan_json_len - 1]["year"] == 6
        assert loan_json[loan_json_len - 1]["endingBalance"] == 0



if __name__ == "__main__":
    unittest.main()