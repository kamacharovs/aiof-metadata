import aiof.fi.core as fi
import aiof.fi.health as fihealth

from aiof.data.fi import *

from fastapi import APIRouter


router = APIRouter()


@router.post("/time")
async def time_to_fi(req: FiTime):
    return fi.time_to_fi(req.startingAmount,
        req.monthlyInvestment,
        req.desiredYearsExpensesForFi,
        req.desiredAnnualSpending)

@router.post("/rule/of/72")
async def rule_of_72(req: FiRuleOf72):
    return fi.rule_of_72(req.startingAmount,
        req.interest)

@router.post("/added/time")
async def added_time(req: FiAddedTime):
    return fi.added_time_to_fi(req.monthlyInvestment,
        req.totalAdditionalExpense)

@router.get("/ten/million/dream/{monthlyInvestment}")
async def ten_million_dream(monthlyInvestment: float):
    return fi.ten_million_dream(monthlyInvestment)

@router.post("/compound/interest")
async def compound_interest(req: FiCompoundInterest):
    return fi.compound_interest(req.startingAmount,
        req.monthlyInvestment,
        req.interest,
        req.numberOfYears,
        req.investmentFees,
        req.taxDrag)

@router.post("/investment/fees/effect")
async def investment_fees_effect(req: FiInvestmentFeesEffect):
    return fi.investment_fees_effect(req.ageAtCareerStart,
        req.interestReturnWhileWorking,
        req.interestReturnWhileRetired,
        req.taxDrag,
        req.annualSavingsFirstDecade,
        req.annualSavingsSecondDecade,
        req.annualWithdrawalThirdDecade)

@router.post("/cost/of/raising/children")
async def cost_of_raising_children(req: FiRaisingChildren):
    return fi.cost_of_raising_children(req.annualExpensesStart,
        req.annualExpensesIncrement,
        req.children,
        req.interests)
@router.get("/cost/of/raising/children/families")
async def cost_of_raising_children_families():
    return fi.cost_of_raising_children_faimilies()

@router.post("/savings/rate")
async def savings_rate(req: SavingsRate):
    return fi.savings_rate(req.salary,
        req.matchAndProfitSharing,
        req.federalIncomeTax,
        req.stateIncomeTax,
        req.fica,
        req.healthAndDentalInsurance,
        req.otherDeductibleBenefits,
        req.hsaInvestment,
        req.fourOhOneKOrFourOhThreeB,
        req.fourFiveSevenB,
        req.sepIra,
        req.otherTaxDeferred,
        req.rothIra,
        req.taxableAccount,
        req.education,
        req.mortgagePrincipal,
        req.studentLoanPrincipal,
        req.otherPostTaxInvestment,
        req.currentNestEgg)


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