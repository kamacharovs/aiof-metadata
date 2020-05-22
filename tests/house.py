import unittest
import json

from aiof.house.core import *


class HouseTestCase(unittest.TestCase):
    """House unit tests"""

    def test_mortgage_calc_yearly(self):
        print(mortgage_calc(250000, 3.25, 30))