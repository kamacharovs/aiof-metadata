import unittest
import json

from aiof.fi.core import *

class FiTestCase(unittest.TestCase):
    """Fi unit tests"""

    def test_time_to_fi_req_defaults(self):
        req = {
            "monthlyInvestment": 5000,
        }
        time_to_fi_resp = time_to_fi_req(req)

        assert time_to_fi_resp["monthlyInvestment"] == 5000
        assert len(time_to_fi_resp["years"]) > 0