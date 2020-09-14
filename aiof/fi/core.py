import numpy_financial as npf
import pandas as pd

# Financial Indepdence (FI) core


# Based on Physician on FIRE calculator
# https://www.physicianonfire.com/timetofi/
def time_to_fi(
    starting_amount=800000,
    monthly_investment=5000,
    desired_years_expenses_for_fi=25,
    desired_annual_spending=100000):
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
                "years": years_to_goal,
            })

    return years_to_goal_obj
