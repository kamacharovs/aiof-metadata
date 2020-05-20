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
        assert True


if __name__ == "__main__":
    unittest.main()