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



    def test_fi_time_to_fi_defaults(self):
        time_to_fi_resp = time_to_fi(
            starting_amount=None,
            monthly_investment=self._monthly_investment,
            desired_years_expenses_for_fi=None,
            desired_annual_spending=None
        )

        assert time_to_fi_resp["monthlyInvestment"] == self._monthly_investment
        assert len(time_to_fi_resp["years"]) > 0
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
        rule_of_72_resp = rule_of_72(
            starting_amount=self._starting_amount,
            interest=None
        )

        assert rule_of_72_resp[0]["startingAmount"] == self._starting_amount
        assert rule_of_72_resp[0]["interest"] == 8
        assert rule_of_72_resp[0]["modifier"] in self._modifier
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



    def test_fi_added_time_to_fi_defaults(self):
        resp = added_time_to_fi(
            monthly_investment=None,
            total_additional_expense=None
        )
        self.assert_fi_added_time_to_fi(resp)
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



    def test_fi_compounded_interest_defaults(self):
        resp = compound_interest(
            starting_amount=None,
            monthly_investment=None,
            interest_rate=None,
            number_of_years=None,
            investment_fees=None,
            tax_drag=None
        )
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



    def test_fi_investment_fees_effect_defaults(self):
        resp = investment_fees_effect(
            age_at_career_start=None,
            interest_return_while_working=None,
            interest_return_while_retired=None,
            tax_drag=None,
            annual_savings_1_decade=None,
            annual_savings_2_decade=None,
            annual_withdrawal_3_decade=None
        )
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



    def test_fi_cost_of_raising_children_defaults(self):
        resp = cost_of_raising_children(
            annual_expenses_start=None,
            annual_expenses_increment=None,
            children=None,
            interests=None
        )
        self.assert_fi_cost_of_raising_children(resp)
    def test_fi_cost_of_raising_children(self):
        resp = cost_of_raising_children(
            annual_expenses_start=10000,
            annual_expenses_increment=5000,
            children=[
                1,
                3,
                5
            ],
            interests=[
                2,
                8
            ])
        self.assert_fi_cost_of_raising_children(resp)

    def assert_fi_cost_of_raising_children(self, resp):
        assert len(resp) > 0
        for cost in resp:
            assert cost["annualExpenses"] > 0
            assert cost["totalExpenses"] > 0
            assert cost["children"] >= 1
            for c in cost["cost"]:
                c["interest"] > 0
                c["value"] > 0



    def test_fi_savings_rate_defaults(self):
        resp = savings_rate(
            salary=None,
            match_and_profit_sharing=None,
            federal_income_tax=None,
            state_income_tax=None,
            fica=None,
            health_and_dental_insurance=None,
            other_deductible_benefits=None,
            hsa_investment=None,
            four_oh_one_k_or_four_oh_three_b=None,
            four_five_seven_b=None,
            sep_ira=None,
            other_tax_deferred=None,
            roth_ira=None,
            taxable_account=None,
            education=None,
            mortgage_principal=None,
            student_loan_principal=None,
            other_post_tax_investment=None,
            current_nest_egg=None)
        self.assert_savings_rate(resp)
    def test_fi_savings_rate(self):
        resp = savings_rate(
            salary=375000,
            match_and_profit_sharing=50000,
            federal_income_tax=50000,
            state_income_tax=10000,
            fica=0,
            health_and_dental_insurance=500,
            other_deductible_benefits=500,
            hsa_investment=500,
            four_oh_one_k_or_four_oh_three_b=19500,
            four_five_seven_b=0,
            sep_ira=0,
            other_tax_deferred=10000,
            roth_ira=6000,
            taxable_account=25000,
            education=0,
            mortgage_principal=0,
            student_loan_principal=0,
            other_post_tax_investment=0,
            current_nest_egg=700000)
        self.assert_savings_rate(resp)

    def assert_savings_rate(self, resp):
        assert len(resp["years"]) > 0
        assert resp["salary"] > 0
        assert resp["matchAndProfitSharing"] > 0
        assert resp["federalIncomeTax"] > 0
        assert resp["stateIncomeTax"] > 0
        assert resp["fica"] >= 0
        assert resp["healthAndDentalInsurance"] > 0
        assert resp["otherDeductibleBenefits"] >= 0
        assert resp["hsaInvestment"] > 0
        assert resp["fourOhOneKOrFourOhThreeB"] > 0
        assert resp["fourFiveSevenB"] >= 0
        assert resp["sepIra"] >= 0
        assert resp["otherTaxDeferred"] >= 0
        assert resp["rothIra"] >= 0
        assert resp["taxableAccount"] >= 0
        assert resp["education"] >= 0
        assert resp["mortgagePrincipal"] >= 0
        assert resp["studentLoanPrincipal"] >= 0
        assert resp["otherPostTaxInvestment"] >= 0
        assert resp["currentNestEgg"] >= 0
        assert resp["postTaxIncome"] >= 0
        assert resp["takeHomePay"] >= 0
        assert resp["annualSpending"] >= 0
        assert resp["allContributions"] >= 0
        assert resp["monthlyContribution"] >= 0
        assert resp["maxPotentialContribution"] >= 0
        assert resp["savingsRateNet"] >= 0
        assert resp["savingsRateGross"] >= 0