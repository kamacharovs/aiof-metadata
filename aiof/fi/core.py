import numpy_financial as npf
import pandas as pd
import math


# Global
_default_round_dig = 2
_interests = [ 
    2,
    4,
    6,
    8
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
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10
]

_frequencies = [
    365,
    12,
    1        
]

_fees = [
    0.10,
    0.50,
    1.00,
    1.50,
    2.00,
    2.50,
    3.00,
]

_children = [
    1,
    2,
    3,
    4
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

    years_to_goal_obj = []
    for interest in _interests:
        years_to_goal = npf.nper(
            (interest / 100)/12, 
            monthly_investment * -1,
            starting_amount * -1,
            desired_retirement_savings_for_fi) / 12

        years_to_goal_obj.append(
            {
                "interest": interest,
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
    starting_amount = req["startingAmount"] if ("startingAmount" in req) and (req["startingAmount"] is not None) else 800000
    monthly_investment = req["monthlyInvestment"] if ("monthlyInvestment" in req) and (req["monthlyInvestment"] is not None) else 5000
    desired_years_expenses_for_fi = req["desiredYearsExpensesForFi"] if ("desiredYearsExpensesForFi" in req) and (req["desiredYearsExpensesForFi"] is not None) else 25
    desired_annual_spending = req["desiredAnnualSpending"] if ("desiredAnnualSpending" in req) and (req["desiredAnnualSpending"] is not None) else 100000
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
            (interest / 100)/12, 
            monthly_investment * -1,
            0,
            total_additional_expense) / 12

        years_added_to_fi_obj.append(
            {
                "interest": interest,
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
                (interest / 100)/12, 
                -monthly_investment,
                0,
                million,
                when='begin') / 12
            million_interests_obj.append({
                    "interest": interest,
                    "years": round(years, 1)
                })
        ten_million_obj.append({
            "million": million,
            "years": million_interests_obj
        })
    return ten_million_obj



# Compound interest
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
        rate = ((interest_rate - investment_fees - tax_drag) / 100) / frequency
        nper = number_of_years * frequency
        pmt = (monthly_investment * 12) / frequency
        fv_begin = -npf.fv(rate, nper, pmt, starting_amount, when='begin')
        fv_end = -npf.fv(rate, nper, pmt, starting_amount, when='end')
        compound_interest_obj.append({
            "startingAmount": starting_amount,
            "monthlyInvestment": monthly_investment,
            "interest": interest_rate,
            "numberOfYears": number_of_years,
            "investmentFees": investment_fees,
            "taxDrag": tax_drag,
            "frequency": frequency,
            "compoundedBeginning": math.ceil(fv_begin),
            "compoundedEnd": math.ceil(fv_end)
        })
    return compound_interest_obj

def compound_interest_req(req):
    starting_amount = req["startingAmount"] if ("startingAmount" in req) and (req["startingAmount"] is not None) else 0
    monthly_investment = req["monthlyInvestment"] if ("monthlyInvestment" in req) and (req["monthlyInvestment"] is not None) else 5000
    interest_rate = req["interest"] if ("interest" in req) and (req["interest"] is not None) else 7
    number_of_years = req["numberOfYears"] if ("numberOfYears" in req) and (req["numberOfYears"] is not None) else 25
    investment_fees = req["investmentFees"] if ("investmentFees" in req) and (req["investmentFees"] is not None) else 0.50
    tax_drag = req["taxDrag"] if ("taxDrag" in req) and (req["taxDrag"] is not None) else 0.50
    return compound_interest(
        starting_amount,
        monthly_investment,
        interest_rate,
        number_of_years,
        investment_fees,
        tax_drag)



# Investment Fees effect
# Enter your data in the gray boxes. If you enter your withdrawal (spending) for the initial decade, the calculator will assume 25% increases for the two decades that follow, 
# then spending is held steady. You may enter your own assumptions for each decade if you prefer
# https://www.physicianonfire.com/calculators/fees-effect-calculator/
def investment_fees_effect(
    age_at_career_start,
    interest_return_while_working,
    interest_return_while_retired,
    tax_drag,
    annual_savings_1_decade,
    annual_savings_2_decade,
    annual_withdrawal_3_decade):
    annual_withdrawal_4_decade = math.ceil(1.25 * annual_withdrawal_3_decade)
    annual_withdrawal_5_decade = math.ceil(1.25 * annual_withdrawal_4_decade)
    annual_withdrawal_6_decade = annual_withdrawal_5_decade
    annual_withdrawal_7_decade = annual_withdrawal_5_decade

    fees_obj = []
    for fee in _fees:
        work_interest_return = (interest_return_while_working - tax_drag - fee) / 100
        retired_interest_return =  (interest_return_while_retired - tax_drag - fee) / 100
        value_obj = []

        fv_after_10_years = -npf.fv(
            work_interest_return / 12,
            120,
            annual_savings_1_decade / 12,
            0,
            when='begin')

        fv_after_20_years = -npf.fv(
            work_interest_return / 12,
            120,
            annual_savings_2_decade / 12,
            fv_after_10_years,
            when='begin')

        retired_fv_30_years = npf.fv(
            retired_interest_return / 12,
            120,
            annual_withdrawal_3_decade / 12,
            -fv_after_20_years,
            when='begin'
        )
        retired_fv_40_years = npf.fv(
            retired_interest_return / 12,
            240,
            annual_withdrawal_4_decade / 12,
            -fv_after_20_years,
            when='begin'
        )
        retired_fv_50_years = npf.fv(
            retired_interest_return / 12,
            360,
            annual_withdrawal_5_decade / 12,
            -fv_after_20_years,
            when='begin'
        )
        retired_fv_60_years = npf.fv(
            retired_interest_return / 12,
            480,
            annual_withdrawal_6_decade / 12,
            -fv_after_20_years,
            when='begin'
        )
        retired_fv_70_years = npf.fv(
            retired_interest_return / 12,
            600,
            annual_withdrawal_7_decade / 12,
            -fv_after_20_years,
            when='begin'
        )

        return_work_interest_return = round(work_interest_return * 100, 1)
        return_retired_interest_return = round(retired_interest_return * 100, 1)
        value_obj.append({
            "age": age_at_career_start + 10, 
            "value": math.ceil(fv_after_10_years),
            "interest": return_work_interest_return
        })
        value_obj.append({
            "age": age_at_career_start + 20, 
            "value": math.ceil(fv_after_20_years),
            "interest": return_work_interest_return
        })
        value_obj.append({
            "age": age_at_career_start + 30, 
            "value": math.ceil(retired_fv_30_years),
            "interest": return_retired_interest_return
        })
        value_obj.append({
            "age": age_at_career_start + 40, 
            "value": math.ceil(retired_fv_40_years),
            "interest": return_retired_interest_return
        })
        value_obj.append({
            "age": age_at_career_start + 50, 
            "value": math.ceil(retired_fv_50_years),
            "interest": return_retired_interest_return
        })
        value_obj.append({
            "age": age_at_career_start + 60, 
            "value": math.ceil(retired_fv_60_years),
            "interest": return_retired_interest_return
        })
        value_obj.append({
            "age": age_at_career_start + 70, 
            "value": math.ceil(retired_fv_70_years),
            "interest": return_retired_interest_return
        })
        fees_obj.append({
            "fee": fee,
            "values": value_obj
        })

    return {
        "ageAtCareerStart": age_at_career_start,
        "interestReturnWhileWorking": interest_return_while_working,
        "interestReturnWhileRetired": interest_return_while_retired,
        "taxDrag": tax_drag,
        "annualSavingsFirstDecade": annual_savings_1_decade,
        "annualSavingsSecondDecade": annual_savings_2_decade,
        "annualSavingsFourthDecade": annual_withdrawal_4_decade,
        "annualSavingsFifthDecade": annual_withdrawal_5_decade,
        "annualSavingsSixthDecade": annual_withdrawal_6_decade,
        "annualSavingsSeventhDecade": annual_withdrawal_7_decade,
        "annualWithdrawalThirdDecade": annual_withdrawal_3_decade,
        "fees": fees_obj
    }

def investment_fees_effect_req(req):
    age_at_career_start = req["ageAtCareerStart"] if "ageAtCareerStart" in req else 32
    interest_return_while_working = req["interestReturnWhileWorking"] if "interestReturnWhileWorking" in req else 8
    interest_return_while_retired = req["interestReturnWhileRetired"] if "interestReturnWhileRetired" in req else 5
    tax_drag = req["taxDrag"] if "taxDrag" in req else 0.3
    annual_savings_1_decade = req["annualSavingsFirstDecade"] if "annualSavingsFirstDecade" in req else 50000
    annual_savings_2_decade = req["annualSavingsSecondDecade"] if "annualSavingsSecondDecade" in req else 100000
    annual_withdrawal_3_decade = req["annualWithdrawalThirdDecade"] if "annualWithdrawalThirdDecade" in req else 70000
    return investment_fees_effect(
        age_at_career_start,
        interest_return_while_working,
        interest_return_while_retired,
        tax_drag,
        annual_savings_1_decade,
        annual_savings_2_decade,
        annual_withdrawal_3_decade)



# Cost of raising children
# This calculator was designed to give you a rough idea of the financial implications of raising children. 
# It is loosely based on the Department of Agriculture’s estimates of raising a child to age 18
# https://www.physicianonfire.com/calculators/cost-of-raising-children/
def cost_of_raising_children(
    annual_expenses_start,
    annual_expenses_increment,
    children,
    interests):
    children_obj = []
    for child in children:
        annual_expenses = 0
        total_expenses = 0
        if child == 1:
            annual_expenses = annual_expenses_start
            total_expenses = annual_expenses_start * 18
        else:
            annual_expenses = annual_expenses_start + (annual_expenses_increment * (child - 1))
            total_expenses = annual_expenses * 18
        
        cost_obj = []
        for interest in interests:
            # nper = 12 months * 18 years
            fv = -npf.fv(
                (interest / 100) / 12,
                216,
                annual_expenses / 12,
                0,
                when='begin')
            cost_obj.append({
                "interest": interest,
                "value": round(fv, _default_round_dig)
            })

        children_obj.append({
            "children": child,
            "annualExpenses": annual_expenses,
            "totalExpenses": total_expenses,
            "cost": cost_obj
        })
    return children_obj

def cost_of_raising_children_faimilies():
    families = [
        {
            "name": "The Frugal Family",
            "annualExpensesStart": 5000,
            "annualExpensesIncrement": 4000,
            "children": _children,
            "interests": _interests
        },
        {
            "name": "The Moderate Sepnders",
            "annualExpensesStart": 9000,
            "annualExpensesIncrement": 5000,
            "children": _children,
            "interests": _interests
        },
        {
            "name": "The Department of Agriculture Estimate",
            "annualExpensesStart": 13000,
            "annualExpensesIncrement": 10000,
            "children": _children,
            "interests": _interests
        },
        {
            "name": "The Upper Crust",
            "annualExpensesStart": 30000,
            "annualExpensesIncrement": 30000,
            "children": _children,
            "interests": _interests
        }
    ]

    families_obj = []
    for family in families:
        children_obj = cost_of_raising_children(
            family["annualExpensesStart"],
            family["annualExpensesIncrement"],
            family["children"],
            family["interests"])
        families_obj.append({
            "name": family["name"],
            "children": children_obj
        })
    return families_obj

def cost_of_raising_children_req(req):
    annual_expenses_start = req["annualExpensesStart"] if ("annualExpensesStart" in req) and (req["annualExpensesStart"] is not None) else 5000
    annual_expenses_increment = req["annualExpensesIncrement"] if ("annualExpensesIncrement" in req) and (req["annualExpensesIncrement"] is not None) else 4000
    children = req["children"] if ("children" in req) and (req["children"] is not None) else _children
    interests = req["interests"] if ("interests" in req) and (req["interests"] is not None) else _interests
    return cost_of_raising_children(
        annual_expenses_start,
        annual_expenses_increment,
        children,
        interests)
