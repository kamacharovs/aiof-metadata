import unittest
import json

from aiof.house.core import *


class HouseTestCase(unittest.TestCase):
    """House unit tests"""

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