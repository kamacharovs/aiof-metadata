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
    _interest_retired = 5
    _modifier = [ 2, 3, 4 ]
    _additional_amount = 450000
    _number_of_years = 25
    _age = 32
    _tax_drag = 0.3
    _savings_first_decade = 50000
    _withdrawal = 70000



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



    def test_fi_added_time_to_fi_req_defaults(self):
        resp = added_time_to_fi_req({})
        self.assert_fi_added_time_to_fi(resp)
    def test_fi_added_time_to_fi_req(self):
        resp = added_time_to_fi_req({
            "monthlyInvestment": self._monthly_investment,
            "totalAdditionalExpense": self._additional_amount
        })
        self.assert_fi_added_time_to_fi(resp)

        for resp_year in resp["years"]:
            assert resp_year["interest"] > 0
            assert resp_year["years"] > 0
    def test_fi_added_time_to_fi(self):
        resp = added_time_to_fi(
            self._monthly_investment,
            self._additional_amount)
        self.assert_fi_added_time_to_fi(resp)

    def assert_fi_added_time_to_fi(self, resp):
        assert resp["monthlyInvestment"] > 0
        assert resp["totalAdditionalExpense"] > 0
        assert len(resp["years"]) > 0
        for resp_year in resp["years"]:
            assert resp_year["interest"] > 0
            assert resp_year["years"] > 0



    def test_fi_ten_million_dream(self):
        resp = ten_million_dream(self._monthly_investment)

        assert len(resp) > 0
        for million in resp:
            assert million["million"] > 0
            for year in million["years"]:
                assert year["interest"] >= 0
                assert year["years"] > 0



    def test_fi_compounded_interest_req_defaults(self):
        resp = compound_interest_req({})
        self.assert_fi_compound_interest(resp)
    def test_fi_compounded_interest_req(self):
        resp = compound_interest_req({
            "startingAmount": 0,
            "monthlyInvestment": self._monthly_investment,
            "interest": self._interest,
            "numberOfYears": self._number_of_years,
            "investmentFees": 0.50,
            "taxDrag": 0.50
        })
        self.assert_fi_compound_interest(resp)
    def test_fi_compounded_interest(self):
        resp = compound_interest(
            starting_amount=0,
            monthly_investment=self._monthly_investment,
            interest_rate=self._interest,
            number_of_years=self._number_of_years,
            investment_fees=0.50,
            tax_drag=0.50)
        self.assert_fi_compound_interest(resp)

    def assert_fi_compound_interest(self, resp):
        assert len(resp) > 0
        for r in resp:
            assert r["compoundedBeginning"] > 0
            assert r["compoundedEnd"] > 0
            assert r["frequency"] > 0
            assert r["interest"] == self._interest or r["interest"] >= self._interest - 1
            assert r["monthlyInvestment"] == self._monthly_investment or r["monthlyInvestment"] >= self._monthly_investment - 2000
            assert r["numberOfYears"] == self._number_of_years
            assert r["startingAmount"] >= 0
            assert r["taxDrag"] >= 0
            assert r["investmentFees"] >= 0



    def test_fi_investment_fees_effect_req_defaults(self):
        resp = investment_fees_effect_req({})
        self.assert_fi_investment_fees_effect(resp)
    def test_fi_investment_fees_effect_req(self):
        resp = investment_fees_effect_req({
            "ageAtCareerStart": self._age,
            "interestReturnWhileWorking": self._interest,
            "interestReturnWhileRetired": self._interest_retired,
            "taxDrag": self._tax_drag,
            "annualSavingsFirstDecade": self._savings_first_decade,
            "annualSavingsSecondDecade": 2 * self._savings_first_decade,
            "annualWithdrawalThirdDecade": self._withdrawal
        })
        self.assert_fi_investment_fees_effect(resp)
    def test_fi_investment_fees_effect(self):
        resp = investment_fees_effect(
            age_at_career_start=self._age,
            interest_return_while_working=self._interest,
            interest_return_while_retired=self._interest_retired,
            tax_drag=self._tax_drag,
            annual_savings_1_decade=self._savings_first_decade,
            annual_savings_2_decade=2 * self._savings_first_decade,
            annual_withdrawal_3_decade=self._withdrawal)
        self.assert_fi_investment_fees_effect(resp)

    def assert_fi_investment_fees_effect(self, resp):
        assert resp["ageAtCareerStart"] == self._age
        assert resp["interestReturnWhileWorking"] == self._interest
        assert resp["interestReturnWhileRetired"] == self._interest_retired
        assert resp["taxDrag"] == self._tax_drag
        assert resp["annualSavingsFirstDecade"] == self._savings_first_decade
        assert resp["annualSavingsSecondDecade"] == 2 * self._savings_first_decade
        assert resp["annualSavingsFourthDecade"] > self._savings_first_decade
        assert resp["annualSavingsFifthDecade"] > self._savings_first_decade
        assert resp["annualSavingsSixthDecade"] > self._savings_first_decade
        assert resp["annualSavingsSeventhDecade"] > self._savings_first_decade
        assert resp["annualWithdrawalThirdDecade"] == self._withdrawal
        assert len(resp["fees"]) > 0
        for fee in resp["fees"]:
            assert fee["fee"] > 0
            for v in fee["values"]:
                assert v["age"] >= self._age
                assert v["interest"] > 0
                assert v["value"] != 0