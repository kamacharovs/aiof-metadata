import aiof.fi.core as fi
import aiof.fi.health as fihealth
import aiof.fi.re as fire

from aiof.data.fi import *

from fastapi import APIRouter


router = APIRouter()


@router.post("/time")
async def time_to_fi(req: FiTime):
    return fi.time_to_fi(
        starting_amount=req.startingAmount,
        monthly_investment=req.monthlyInvestment,
        desired_years_expenses_for_fi=req.desiredYearsExpensesForFi,
        desired_annual_spending=req.desiredAnnualSpending
    )

@router.post("/rule/of/72")
async def rule_of_72(req: FiRuleOf72):
    return fi.rule_of_72(
        starting_amount=req.startingAmount,
        interest=req.interest
    )

@router.post("/added/time")
async def added_time(req: FiAddedTime):
    return fi.added_time_to_fi(
        monthly_investment=req.monthlyInvestment,
        total_additional_expense=req.totalAdditionalExpense
    )

@router.get("/ten/million/dream/{monthlyInvestment}")
async def ten_million_dream(monthlyInvestment: float):
    return fi.ten_million_dream(monthly_investment=monthlyInvestment)

@router.post("/compound/interest")
async def compound_interest(req: FiCompoundInterest):
    return fi.compound_interest(
        starting_amount=req.startingAmount,
        monthly_investment=req.monthlyInvestment,
        interest_rate=req.interest,
        number_of_years=req.numberOfYears,
        investment_fees=req.investmentFees,
        tax_drag=req.taxDrag
    )

@router.post("/investment/fees/effect")
async def investment_fees_effect(req: FiInvestmentFeesEffect):
    return fi.investment_fees_effect(
        age_at_career_start=req.ageAtCareerStart,
        interest_return_while_working=req.interestReturnWhileWorking,
        interest_return_while_retired=req.interestReturnWhileRetired,
        tax_drag=req.taxDrag,
        annual_savings_1_decade=req.annualSavingsFirstDecade,
        annual_savings_2_decade=req.annualSavingsSecondDecade,
        annual_withdrawal_3_decade=req.annualWithdrawalThirdDecade
    )

@router.post("/cost/of/raising/children")
async def cost_of_raising_children(req: FiRaisingChildren):
    return fi.cost_of_raising_children(
        annual_expenses_start=req.annualExpensesStart,
        annual_expenses_increment=req.annualExpensesIncrement,
        children=req.children,
        interests=req.interests
    )
@router.get("/cost/of/raising/children/families")
async def cost_of_raising_children_families():
    return fi.cost_of_raising_children_faimilies()

@router.post("/savings/rate")
async def savings_rate(req: SavingsRate):
    return fi.savings_rate(
        salary=req.salary,
        match_and_profit_sharing=req.matchAndProfitSharing,
        federal_income_tax=req.federalIncomeTax,
        state_income_tax=req.stateIncomeTax,
        fica=req.fica,
        health_and_dental_insurance=req.healthAndDentalInsurance,
        other_deductible_benefits=req.otherDeductibleBenefits,
        hsa_investment=req.hsaInvestment,
        four_oh_one_k_or_four_oh_three_b=req.fourOhOneKOrFourOhThreeB,
        four_five_seven_b=req.fourFiveSevenB,
        sep_ira=req.sepIra,
        other_tax_deferred=req.otherTaxDeferred,
        roth_ira=req.rothIra,
        taxable_account=req.taxableAccount,
        education=req.education,
        mortgage_principal=req.mortgagePrincipal,
        student_loan_principal=req.studentLoanPrincipal,
        other_post_tax_investment=req.otherPostTaxInvestment,
        current_nest_egg=req.currentNestEgg
    )


@router.post("/health/bmi/imperial")
async def bmi_imperial(req: BmiImperial):
    return fihealth.bmi_imperial(
        weight=req.weight,
        feet=req.feet,
        inches=req.inches
    )

@router.post("/health/bmi/metric")
async def bmi_metric(req: BmiMetric):
    return fihealth.bmi_metric(
        weight=req.weight,
        height=req.height
    )


@router.get("/re/sample")
async def re_sample():
    return fire.coast_fire_savings()