import unittest
import json

from aiof.fi.core import *

class FiTestCase(unittest.TestCase):
    """Fi unit tests"""

    _starting_amount = 350000
    _monthly_investment = 7000
    _desired_years_expenses_for_fi = 30
    _desired_annual_spending = 100000
    _interest = 8
    _modifier = [ 2, 3, 4 ]

    def test_fi_time_to_fi_req_defaults(self):
        req = {
            "monthlyInvestment": self._monthly_investment,
        }
        time_to_fi_resp = time_to_fi_req(req)

        assert time_to_fi_resp["monthlyInvestment"] == self._monthly_investment
        assert len(time_to_fi_resp["years"]) > 0
    def test_fi_time_to_fi_req(self):
        req = {
            "startingAmount": self._starting_amount,
            "monthlyInvestment": self._monthly_investment,
            "desiredYearsExpensesForFi": self._desired_years_expenses_for_fi,
            "desiredAnnualSpending": self._desired_annual_spending
        }
        time_to_fi_resp = time_to_fi_req(req)

        assert time_to_fi_resp["startingAmount"] == self._starting_amount
        assert time_to_fi_resp["monthlyInvestment"] == self._monthly_investment
        assert time_to_fi_resp["desiredYearsExpensesForFi"] == self._desired_years_expenses_for_fi
        assert time_to_fi_resp["desiredAnnualSpending"] == self._desired_annual_spending
        assert len(time_to_fi_resp["years"]) > 0

        for years in time_to_fi_resp["years"]:
            assert years["interest"] > 0
            assert years["years"] > 0
    def test_fi_time_to_fi(self):
        time_to_fi_resp = time_to_fi(
            self._starting_amount, 
            self._monthly_investment, 
            self._desired_years_expenses_for_fi, 
            self._desired_annual_spending)
        
        assert time_to_fi_resp["startingAmount"] == self._starting_amount
        assert time_to_fi_resp["monthlyInvestment"] == self._monthly_investment
        assert time_to_fi_resp["desiredYearsExpensesForFi"] == self._desired_years_expenses_for_fi
        assert time_to_fi_resp["desiredAnnualSpending"] == self._desired_annual_spending
        assert len(time_to_fi_resp["years"]) > 0

        for years in time_to_fi_resp["years"]:
            assert years["interest"] > 0
            assert years["years"] > 0



    def test_fi_rule_of_72_req_defaults(self):
        req = {
            "startingAmount": self._starting_amount
        }
        rule_of_72_resp = rule_of_72_req(req)

        assert rule_of_72_resp[0]["startingAmount"] == self._starting_amount
        assert rule_of_72_resp[0]["interest"] == 8
        assert rule_of_72_resp[0]["modifier"] in self._modifier
    def test_fi_rule_of_72_req(self):
        req = {
            "startingAmount": self._starting_amount,
            "interest": self._interest
        }
        rule_of_72_resp = rule_of_72_req(req)

        for resp in rule_of_72_resp:
            assert resp["startingAmount"] == self._starting_amount
            assert resp["interest"] == self._interest
            assert resp["modifier"] in self._modifier
            assert resp["endingAmount"] == resp["startingAmount"] * resp["modifier"]
            assert resp["years"] > 0
    def test_fi_rule_of_72(self):
        rule_of_72_resp = rule_of_72(
            self._starting_amount,
            self._interest
        )

        for resp in rule_of_72_resp:
            assert resp["startingAmount"] == self._starting_amount
            assert resp["interest"] == self._interest
            assert resp["modifier"] in self._modifier
            assert resp["endingAmount"] == resp["startingAmount"] * resp["modifier"]
            assert resp["years"] > 0