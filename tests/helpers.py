import unittest

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


if __name__ == "__main__":
    unittest.main()