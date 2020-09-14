import numpy_financial as npf
import pandas as pd


# Based on Physician on FIRE calculator
# https://www.physicianonfire.com/timetofi/
def time_to_fi(
    starting_amount=800000,
    monthly_investment=5000,
    desired_years_expenses_for_fi=25,
    desired_annual_spending=100000):
    desired_retirement_savings_for_fi = desired_years_expenses_for_fi * desired_annual_spending
    current_deficit = desired_retirement_savings_for_fi - starting_amount

    years_to_goal_at_2_perc = npf.nper(
        0.02/12, 
        monthly_investment * -1,
        starting_amount * -1,
        desired_retirement_savings_for_fi) / 12

    print(years_to_goal_at_2_perc)
