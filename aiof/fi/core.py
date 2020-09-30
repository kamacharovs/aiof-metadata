import numpy_financial as npf
import pandas as pd
import math

import aiof.config as config


# Configs
_settings = config.Settings()
_default_round_dig = _settings.DefaultRoundingDigit
_interests = _settings.DefaultInterests
_frequencies = _settings.DefaultFrequencies
_fees = _settings.DefaultFees
_children = _settings.DefaultChildren
_ten_million = _settings.DefaultTenMillion
_ten_million_interests = _settings.DefaultTenMillionInterests


# Financial Indepdence (FI) core


# Based on Physician on FIRE calculator
# https://www.physicianonfire.com/timetofi/
def time_to_fi(
    starting_amount,
    monthly_investment,
    desired_years_expenses_for_fi,
    desired_annual_spending):
    starting_amount = starting_amount if starting_amount is not None else 800000
    monthly_investment = monthly_investment if monthly_investment is not None else 5000
    desired_years_expenses_for_fi = desired_years_expenses_for_fi if desired_years_expenses_for_fi is not None else 25
    desired_annual_spending = desired_annual_spending if desired_annual_spending is not None else 100000

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


# Rule of 72
# Based on Physician on FIRE calculator
# https://www.physicianonfire.com/calculators/72calculator/
def rule_of_72(
    starting_amount,
    interest):
    starting_amount = round(starting_amount) if starting_amount is not None else 100000
    interest = interest if interest is not None else 8

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


# Added time to FI
# This calculator was designed to help you determine how much an additional expense (such as having children) can add to your FI timeline.
# Plug in the grand total of the additional expense and the amount you invest monthly to cover it
def added_time_to_fi(
    monthly_investment,
    total_additional_expense):
    monthly_investment = round(monthly_investment) if monthly_investment is not None else 10000
    total_additional_expense = round(total_additional_expense) if total_additional_expense is not None else 422000

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
    investment_fees,
    tax_drag):
    starting_amount = starting_amount if starting_amount is not None else 0
    monthly_investment = monthly_investment if monthly_investment is not None else 5000
    interest_rate = interest_rate if interest_rate is not None else 7
    number_of_years = number_of_years if number_of_years is not None else 25
    investment_fees = investment_fees if investment_fees is not None else 0.50
    tax_drag = tax_drag if tax_drag is not None else 0.50

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
    age_at_career_start = age_at_career_start if age_at_career_start is not None else 32
    interest_return_while_working = interest_return_while_working if interest_return_while_working is not None else 8
    interest_return_while_retired = interest_return_while_retired if interest_return_while_retired is not None else 5
    tax_drag = tax_drag if tax_drag is not None else 0.3
    annual_savings_1_decade = annual_savings_1_decade if annual_savings_1_decade is not None else 50000
    annual_savings_2_decade = annual_savings_2_decade if annual_savings_2_decade is not None else 100000
    annual_withdrawal_3_decade = annual_withdrawal_3_decade if annual_withdrawal_3_decade is not None else 70000

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


# Cost of raising children
# This calculator was designed to give you a rough idea of the financial implications of raising children. 
# It is loosely based on the Department of Agriculture’s estimates of raising a child to age 18
# https://www.physicianonfire.com/calculators/cost-of-raising-children/
def cost_of_raising_children(
    annual_expenses_start,
    annual_expenses_increment,
    children,
    interests):
    annual_expenses_start = annual_expenses_start if annual_expenses_start is not None else 5000
    annual_expenses_increment = annual_expenses_increment if annual_expenses_increment is not None else 4000
    children = children if children is not None else _children
    interests = interests if interests is not None else _interests

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


# Savings rate
# don’t think there’s a right or a wrong way to calculate your savings, this is just a tool to give you a better idea of how much you are saving (and spending) each year.
# Spending is calculated automatically. It assumes that all dollars unaccounted for elsewhere are spent, so this savings calculator doubles as a spending calculator
# NOTE: assumes future spending requirements equals this year's spending
# https://www.physicianonfire.com/calculators/savings-calculator/
def savings_rate(
    salary,
    match_and_profit_sharing,
    federal_income_tax,
    state_income_tax,
    fica,
    health_and_dental_insurance,
    other_deductible_benefits,
    hsa_investment,
    four_oh_one_k_or_four_oh_three_b,
    four_five_seven_b,
    sep_ira,
    other_tax_deferred,
    roth_ira,
    taxable_account,
    education,
    mortgage_principal,
    student_loan_principal,
    other_post_tax_investment,
    current_nest_egg):
    salary = salary if salary is not None else 300000
    match_and_profit_sharing = match_and_profit_sharing if match_and_profit_sharing is not None else 20000
    federal_income_tax = federal_income_tax if federal_income_tax is not None else 50000
    state_income_tax = state_income_tax if state_income_tax is not None else 10000
    fica = fica if fica is not None else 12000
    compensation = salary + match_and_profit_sharing
    income_taxes = federal_income_tax + state_income_tax + fica
    post_tax_income = salary - income_taxes

    # Pre-tax spending
    health_and_dental_insurance = health_and_dental_insurance if health_and_dental_insurance is not None else 15000
    other_deductible_benefits = other_deductible_benefits if other_deductible_benefits is not None else 0
    pre_tax_spendings = health_and_dental_insurance + other_deductible_benefits

    # Pre-tax investments
    hsa_investment = hsa_investment if hsa_investment is not None else 7000
    four_oh_one_k_or_four_oh_three_b = four_oh_one_k_or_four_oh_three_b if four_oh_one_k_or_four_oh_three_b is not None else 19500
    four_five_seven_b = four_five_seven_b if four_five_seven_b is not None else 19500
    sep_ira = sep_ira if sep_ira is not None else 0
    other_tax_deferred = other_tax_deferred if other_tax_deferred is not None else 0
    pre_tax_investments = hsa_investment + four_oh_one_k_or_four_oh_three_b + four_five_seven_b + sep_ira + other_tax_deferred

    # Post-tax investments
    roth_ira = roth_ira if roth_ira is not None else 12000
    taxable_account = taxable_account if taxable_account is not None else 16000
    education = education if education is not None else 10000
    mortgage_principal = mortgage_principal if mortgage_principal is not None else 18000
    student_loan_principal = student_loan_principal if student_loan_principal is not None else 12000
    other_post_tax_investment = other_post_tax_investment if other_post_tax_investment is not None else 0
    post_tax_investments = roth_ira + taxable_account + education + mortgage_principal + student_loan_principal + other_post_tax_investment

    current_nest_egg = current_nest_egg if current_nest_egg is not None else 0

    # Totals
    take_home_pay = post_tax_income - pre_tax_spendings - pre_tax_investments
    annual_spending = take_home_pay - post_tax_investments
    all_contributions = match_and_profit_sharing + pre_tax_investments + post_tax_investments
    monthly_contribution = all_contributions / 12
    max_potential_contribution = take_home_pay + match_and_profit_sharing + pre_tax_investments
    savings_rate_net = (all_contributions / max_potential_contribution ) * 100
    savings_rate_gross = (all_contributions / compensation ) * 100
    required_nest_egg_for_fi = annual_spending * 25

    years_obj = []
    for interest in _interests:
        years_to_fi = npf.nper(
            (interest / 100) / 12,
            -monthly_contribution,
            -current_nest_egg,
            required_nest_egg_for_fi,
            when='end') / 12
        years_obj.append({
            "interest": interest,
            "years": round(years_to_fi, _default_round_dig)
        })

    return {
        "salary": salary,
        "matchAndProfitSharing": match_and_profit_sharing,
        "federalIncomeTax": federal_income_tax,
        "stateIncomeTax": state_income_tax,
        "fica": fica,
        "healthAndDentalInsurance": health_and_dental_insurance,
        "otherDeductibleBenefits": other_deductible_benefits,
        "hsaInvestment": hsa_investment,
        "fourOhOneKOrFourOhThreeB": four_oh_one_k_or_four_oh_three_b,
        "fourFiveSevenB": four_five_seven_b,
        "sepIra": sep_ira,
        "otherTaxDeferred": other_tax_deferred,
        "rothIra": roth_ira,
        "taxableAccount": taxable_account,
        "education": education,
        "mortgagePrincipal": mortgage_principal,
        "studentLoanPrincipal": student_loan_principal,
        "otherPostTaxInvestment": other_post_tax_investment,
        "currentNestEgg": current_nest_egg,

        "postTaxIncome": round(post_tax_income, _default_round_dig),
        "takeHomePay": round(take_home_pay, _default_round_dig),
        "annualSpending": round(annual_spending, _default_round_dig),
        "allContributions": round(all_contributions, _default_round_dig),
        "monthlyContribution": round(monthly_contribution, _default_round_dig),
        "maxPotentialContribution": round(max_potential_contribution, _default_round_dig),
        "savingsRateNet": round(savings_rate_net, _default_round_dig),
        "savingsRateGross": round(savings_rate_gross, _default_round_dig),
        "years": years_obj
    }
    