import unittest

from .context import aiof


class HelpersTestSuite(unittest.TestCase):
    """Helpers unit tests"""

    def test_convert_frequency_daily(self):
        assert aiof.convert_frequency("daily") == 365


if __name__ == "__main__":
    unittest.main()