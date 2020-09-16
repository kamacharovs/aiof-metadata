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
        
    def test_time_to_fi_req(self):
        req = {
            "startingAmount": 350000,
            "monthlyInvestment": 7000,
            "desiredYearsExpensesForFi": 30,
            "desiredAnnualSpending": 100000
        }
        time_to_fi_resp = time_to_fi_req(req)

        assert time_to_fi_resp["startingAmount"] == 350000
        assert time_to_fi_resp["monthlyInvestment"] == 7000
        assert time_to_fi_resp["desiredYearsExpensesForFi"] == 30
        assert time_to_fi_resp["desiredAnnualSpending"] == 100000
        assert len(time_to_fi_resp["years"]) > 0

        for years in time_to_fi_resp["years"]:
            assert years["interest"] > 0
            assert years["years"] > 0

    def test_time_to_fi(self):
        starting_amount = 350000
        monthly_investment = 7000
        desired_years_expenses_for_fi = 30
        desired_annual_spending = 100000
        time_to_fi_resp = time_to_fi(
            starting_amount, 
            monthly_investment, 
            desired_years_expenses_for_fi, 
            desired_annual_spending)
        
        assert time_to_fi_resp["startingAmount"] == 350000
        assert time_to_fi_resp["monthlyInvestment"] == 7000
        assert time_to_fi_resp["desiredYearsExpensesForFi"] == 30
        assert time_to_fi_resp["desiredAnnualSpending"] == 100000
        assert len(time_to_fi_resp["years"]) > 0

        for years in time_to_fi_resp["years"]:
            assert years["interest"] > 0
            assert years["years"] > 0