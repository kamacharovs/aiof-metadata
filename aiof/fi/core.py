import numpy_financial as npf
import pandas as pd


# Global
_interests = [ 
    0.02,
    0.04,
    0.06,
    0.08
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
