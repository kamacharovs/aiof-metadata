import math
import numpy_financial as npf
import pandas as pd

import aiof.config as config

from typing import List


# Configs
_settings = config.get_settings()
_round_dig = _settings.DefaultRoundingDigit
_interests = _settings.DefaultInterests
_frequencies = _settings.DefaultFrequencies
_fees = _settings.DefaultFees
_children = _settings.DefaultChildren
_ten_million = _settings.DefaultTenMillion
_ten_million_interests = _settings.DefaultTenMillionInterests


# Financial Indepdence (FI) core


def time_to_fi(
    starting_amount: float,
    monthly_investment: float,
    desired_years_expenses_for_fi: int,
    desired_annual_spending: float):
    """
    Find out how many years you have left in your path to FI (financial independence) at various real returns on your investments

    Parameters
    ----------
    `starting_amount` : float or None.
        starting amount. defaults to `800,000`\n
    `monthly_investment` : float or None.
        monthly investment over the years. defaults to `5,000`\n
    `desired_years_expenses_for_fi` : int or None.
        desired years of expenses after one retires. defaults to `25`\n
    `desired_annual_spending` : float or None.
        desired annual spending amount after one retires. defaults to `100,000`

    Notes
    ----------
    Based on Physician on FIRE's calculator: https://www.physicianonfire.com/timetofi/
    """
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


def rule_of_72(
    starting_amount: float,
    interest: float):
    """
    Estimates how long a lump sum of money will take to double. As a bonus, the Rule of 114 for tripling your money, and the Rule of 144 for quadrupling your money are included

    Parameters
    ----------
    `starting_amount` : float or None.
        starting amount. defaults to `100,000`\n
    `interest` : float or None.
        interest rate. defaults to `8`

    Notes
    ----------
    Based on Physician on FIRE's calculator: https://www.physicianonfire.com/calculators/72calculator/
    """
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


def added_time_to_fi(
    monthly_investment: float,
    total_additional_expense: float):
    """
    Determine how much an additional expense (such as having children) can add to your FI (financial independence) timeline

    Parameters
    ----------
    `monthly_investment` : float or None.
        monthly investment over the years. defaults to `10,000`\n
    `total_additional_expense` : float or None.
        total additional expense. defaults to `422,000`

    Notes
    ----------
    Based on Physician on FIRE's calculator: https://www.physicianonfire.com/calculators/added-time-fi-calculator/
    """
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


def ten_million_dream(monthly_investment: float):
    """
    Determine the number of years to reach a savings goal based on a variety of market returns

    Parameters
    ----------
    `monthly_investment` : float or None.
        monthly investment over the years. defaults to `10,000`

    Notes
    ----------
    Based on Physician on FIRE's calculator: https://www.physicianonfire.com/calculators/10-million-dream/
    """
    monthly_investment = monthly_investment if monthly_investment is not None else 10000

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


def compound_interest(
    starting_amount: float,
    monthly_investment: float,
    interest_rate: float,
    number_of_years: int,
    investment_fees: float,
    tax_drag: float):
    """
    Compound interest calculator. Results are displayed representing daily, monthly, and annual compounding, 
    with additions made at the beginning or end of the day, month or year

    Parameters
    ----------
    `starting_amount` : float or None.
        starting amount. defaults to `0`\n
    `monthly_investment` : float or None.
        monthly investment over the years. defaults to `5,000`\n
    `interest_rate` : float or None.
        interest rate at which the compounding is calculated. defaults to `7`\n
    `number_of_years` : int or None.
        number of years for which the compounding is calculated. defaults to `25`\n
    `investment_fees` : float or None.
        investment fees (if any) to subtract from the interest rate. defaults to `0.50`\n
    `tax_drag` : float or None.
        tax drag (if any) to subtract from the interest rate. defaults to `0.50`

    Notes
    ----------
    Based on Physician on FIRE's calculator: https://www.physicianonfire.com/calculators/compound/
    """
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


def investment_fees_effect(
    age_at_career_start: int,
    interest_return_while_working: float,
    interest_return_while_retired: float,
    tax_drag: float,
    annual_savings_1_decade: float,
    annual_savings_2_decade: float,
    annual_withdrawal_3_decade: float):
    """
    Effects of investment fees

    Parameters
    ----------
    `age_at_career_start` : int or None.
        age at which one's career has started. defaults to `32`\n
    `interest_return_while_working` : float or None.
        interest rate while one is working. defaults to `8`\n
    `interest_return_while_retired` : float or None.
        interest rate while one is retired. defaults to `5`\n
    `tax_drag` : float or None.
        tax drag (if any) to subtract from the interest rate. defaults to `0.30`\n
    `annual_savings_1_decade` : float or None.
        the amount of savings in the 1st decade of working. defaults to `50,000`\n
    `annual_savings_2_decade` : float or None.
        the amount of savings in the 2nd decade of working. defaults to `100,000`\n
    `annual_withdrawal_3_decade` : float or None.
        the amount of withdrawal in the 3rd decade of retirement. the other decades are calculated accordingly - 
        additional percentages. defaults to `70,000`\n

    Notes
    ----------
    Based on Physician on FIRE's calculator: https://www.physicianonfire.com/calculators/fees-effect-calculator/
    """
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


def cost_of_raising_children(
    annual_expenses_start: float = None,
    annual_expenses_increment: float = None,
    children: List[int] = None,
    interests: List[int] = None,
    years: int = 18):
    """
    This calculator was designed to give you a rough idea of the financial implications of raising children. 
    It is loosely based on the Department of Agriculture’s estimates of raising a child to age 18

    Parameters
    ----------
    `annual_expenses_start` : float
        annual expenses start per child. defaults to `5,000`\n
    `annual_expenses_increment` : float or None.
        annual expenses increment per child. defaults to `5,000`\n
    `children` : list or None.
        the number of children for which to calculate the cost of raising. defaults to `[1,2,3,4]`\n
    `interests` : list or None.
        the interest rates at which to calculate the opportunity cost. defaults to `[2,4,6,8]`\n
    `years` : int or 18.
        the number of years to calculate the cost on. defaults to `18`

    Notes
    ----------
    Based on Physician on FIRE's calculator: https://www.physicianonfire.com/calculators/cost-of-raising-children/
    """
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
            fv = -npf.fv(
                (interest / 100) / 12,
                years * 12,
                annual_expenses / 12,
                0,
                when='begin')
            cost_obj.append({
                "interest": interest,
                "value": round(fv, _round_dig)
            })

        children_obj.append({
            "children": child,
            "years": years,
            "annualExpenses": round(annual_expenses, _round_dig),
            "totalExpenses": round(total_expenses, _round_dig),
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


def savings_rate(
    salary: float,
    match_and_profit_sharing: float,
    federal_income_tax: float,
    state_income_tax: float,
    fica: float,
    health_and_dental_insurance: float,
    other_deductible_benefits: float,
    hsa_investment: float,
    four_oh_one_k_or_four_oh_three_b: float,
    four_five_seven_b: float,
    sep_ira: float,
    other_tax_deferred: float,
    roth_ira: float,
    taxable_account: float,
    education: float,
    mortgage_principal: float,
    student_loan_principal: float,
    other_post_tax_investment: float,
    current_nest_egg: float):
    """
    Calculate one's savings rate

    Notes
    ----------
    Based on Physician on FIRE's calculator: https://www.physicianonfire.com/calculators/savings-calculator/
    """
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
            "years": round(years_to_fi, _round_dig)
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

        "postTaxIncome": round(post_tax_income, _round_dig),
        "takeHomePay": round(take_home_pay, _round_dig),
        "annualSpending": round(annual_spending, _round_dig),
        "allContributions": round(all_contributions, _round_dig),
        "monthlyContribution": round(monthly_contribution, _round_dig),
        "maxPotentialContribution": round(max_potential_contribution, _round_dig),
        "savingsRateNet": round(savings_rate_net, _round_dig),
        "savingsRateGross": round(savings_rate_gross, _round_dig),
        "years": years_obj
    }
    