import unittest
import json

from aiof.fi.health import bmi_imperial


class FiHealthTestCase(unittest.TestCase):
    """Fi health unit tests"""

    _starting_amount = 350000


    def test_bmi_imperial_defaults(self):
        bmi = bmi_imperial(
            weight=None,
            feet=None,
            inches=None)
            
        assert bmi > 0