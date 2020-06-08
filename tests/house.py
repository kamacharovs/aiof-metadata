import unittest
import json

from aiof.house.core import *


class HouseTestCase(unittest.TestCase):
    """House unit tests"""

    def test_mortgage_calc_yearly(self):
        assert house_mortgage_calc(250000, 3.25, 30) > 0


    def test_house_future_value_calc(self):
        assert round(house_future_value_calc(1000, 2, 5), 2) == 5204.04