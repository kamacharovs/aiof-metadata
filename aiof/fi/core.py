import numpy_financial as npf
import pandas as pd
import math


# Global
_interests = [ 
    0.02,
    0.04,
    0.06,
    0.08
]

_ten_million = [
    1000000,
    2000000,
    3000000,
    4000000,
    5000000,
    6000000,
    7000000,
    8000000,
    9000000,
    10000000,
    100000000,
]
_ten_million_interests = [
    0,
    0.01,
    0.02,
    0.03,
    0.04,
    0.05,
    0.06,
    0.07,
    0.08,
    0.09,
    0.10
]

_frequencies = [
    365,
    12,
    1        
]


# Financial Indepdence (FI) core


# Based on Physician on FIRE calculator
# https://www.physicianonfire.com/timetofi/
def time_to_fi(
    starting_amount,
    monthly_investment,
    desired_years_expenses_for_fi,
    desired_annual_spending):
    desired_retirement_savings_for_fi = desired_years_expenses_for_fi * desired_annual_spending
    current_deficit = desired_retirement_savings_for_fi - starting_amount

    interests = [ 
        0.02,
        0.04,
        0.06,
        0.08
    ]

    years_to_goal_obj = []
    for interest in interests:
        years_to_goal = npf.nper(
            interest/12, 
            monthly_investment * -1,
            starting_amount * -1,
            desired_retirement_savings_for_fi) / 12

        years_to_goal_obj.append(
            {
                "interest": interest * 100,
                "years": round(years_to_goal, 1),
            })

    return {
        "startingAmount": starting_amount,
        "monthlyInvestment": monthly_investment,
        "desiredYearsExpensesForFi": desired_years_expenses_for_fi,
        "desiredAnnualSpending": desired_annual_spending,
        "desiredRetirementSavingsForFi": desired_retirement_savings_for_fi,
        "currentDeficit": current_deficit,
        "years": years_to_goal_obj
    }

def time_to_fi_req(req):
    starting_amount = req["startingAmount"] if "startingAmount" in req else 800000
    monthly_investment = req["monthlyInvestment"] if "monthlyInvestment" in req else 5000
    desired_years_expenses_for_fi = req["desiredYearsExpensesForFi"] if "desiredYearsExpensesForFi" in req else 25
    desired_annual_spending = req["desiredAnnualSpending"] if "desiredAnnualSpending" in req else 100000
    return time_to_fi(
        starting_amount,
        monthly_investment,
        desired_years_expenses_for_fi,
        desired_annual_spending)



# Rule of 72
# Based on Physician on FIRE calculator
# https://www.physicianonfire.com/calculators/72calculator/
def rule_of_72(
    starting_amount,
    interest):
    rules = dict({ 
        72: 2,
        114: 3,
        144: 4
    })
    years_obj = []

    for key in rules:
        modified_value = starting_amount * rules[key]
        years = round(key/interest, 1)
        years_obj.append(
            {
                "startingAmount": starting_amount,
                "interest": interest,
                "modifier": rules[key],
                "endingAmount": modified_value,
                "years": years,
            })

    return years_obj

def rule_of_72_req(req):
    starting_amount = req["startingAmount"] if "startingAmount" in req else 100000
    interest = req["interest"] if "interest" in req else 8
    return rule_of_72(
        starting_amount,
        interest)



# Added time to FI
# This calculator was designed to help you determine how much an additional expense (such as having children) can add to your FI timeline.
# Plug in the grand total of the additional expense and the amount you invest monthly to cover it
def added_time_to_fi(
    monthly_investment,
    total_additional_expense):
    years_added_to_fi_obj = []

    for interest in _interests:
        years_added = npf.nper(
            interest/12, 
            monthly_investment * -1,
            0,
            total_additional_expense) / 12

        years_added_to_fi_obj.append(
            {
                "interest": interest * 100,
                "years": round(years_added, 1),
            })

    return {
        "monthlyInvestment": monthly_investment,
        "totalAdditionalExpense": total_additional_expense,
        "years": years_added_to_fi_obj
    }

def added_time_to_fi_req(req):
    monthly_investment = req["monthlyInvestment"] if "monthlyInvestment" in req else 10000
    total_additional_expense = req["totalAdditionalExpense"] if "totalAdditionalExpense" in req else 422000
    return added_time_to_fi(
        monthly_investment,
        total_additional_expense)



# $10m dream
# This calculator, developed in the post about Dr. F’s $10 Million dream, will determine the number of years to reach a savings goal based on a variety of market returns
# https://www.physicianonfire.com/calculators/10-million-dream/
def ten_million_dream(monthly_investment):
    ten_million_obj = []
    for million in _ten_million:
        million_interests_obj = []
        for interest in _ten_million_interests:
            years = npf.nper(
                interest/12, 
                -monthly_investment,
                0,
                million,
                when='begin') / 12
            million_interests_obj.append({
                    "interest": round(interest * 100, 1),
                    "years": round(years, 1)
                })
        ten_million_obj.append({
            "million": million,
            "years": million_interests_obj
        })
    return ten_million_obj



# Compound
# Enter your data in the white cells. Six results are displayed representing daily, monthly, and annual compounding, with additions made at the beginning or end of the day, month or year
# https://www.physicianonfire.com/calculators/compound/
#
# investment_fees : Including expense ratios, fund loads, AUM fees, etc… (0.1% to 3%)
# tax_drag        : For taxable account only (typical range of 0.3% to 1%)
def compound_interest(
    starting_amount,
    monthly_investment,
    interest_rate,
    number_of_years,
    investment_fees=0,
    tax_drag=0):
    compound_interest_obj = []
    for frequency in _frequencies:
        fv = -npf.fv(
            ((interest_rate - investment_fees - tax_drag) / 100) / frequency,
            number_of_years * frequency,
            (monthly_investment * 12) / frequency,
            starting_amount,
            when='begin')
        compound_interest_obj.append({
            "startingAmount": starting_amount,
            "monthlyInvestment": monthly_investment,
            "interest": interest_rate,
            "numberOfYears": number_of_years,
            "investmentFees": investment_fees,
            "taxDrag": tax_drag,
            "frequency": frequency,
            "compounded": math.ceil(fv)
        })
    return compound_interest_obj

def compound_interest_req(req):
    starting_amount = req["startingAmount"] if "startingAmount" in req else 0
    monthly_investment = req["monthlyInvestment"] if "monthlyInvestment" in req else 5000
    interest_rate = req["interest"] if "interest" in req else 7
    number_of_years = req["numberOfYears"] if "numberOfYears" in req else 25
    investment_fees = req["investmentFees"] if "investmentFees" in req else 0.50
    tax_drag = req["taxDrag"] if "taxDrag" in req else 0.50
    return compound_interest(
        starting_amount,
        monthly_investment,
        interest_rate,
        number_of_years,
        investment_fees,
        tax_drag)
