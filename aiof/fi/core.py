import numpy_financial as npf
import pandas as pd

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
    double_value = starting_amount * 2
    return {
        "startingAmount": starting_amount,
        "interest": interest,
        "double": double_value,
        "years": round(72/interest, 1),
    }

def rule_of_72_req(req):
    starting_amount = req["startingAmount"] if "startingAmount" in req else 100000
    interest = req["interest"] if "interest" in req else 8
    return rule_of_72(
        starting_amount,
        interest)
