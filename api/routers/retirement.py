import aiof.retirement.core as retirement

from aiof.data.retirement import WithdrawalRequest, CommonInvestmentsRequest
from aiof.data.retirement import NumberSimpleRequest, NumberRequest

from fastapi import APIRouter


router = APIRouter()


@router.post("/withdrawal")
async def withdrawal_calc_async(req: WithdrawalRequest):
    return retirement.withdrawal_calc(
        retirement_number   = req.retirementNumber,
        take_out_percentage = req.takeOutPercentage,
        number_of_years     = req.numberOfYears,
        as_json             = True)

@router.post("/common/investments")
async def common_investments_async(req: CommonInvestmentsRequest):
    return retirement.common_investments(
        interest                            = req.interest,
        start_year                          = req.startYear,
        end_year                            = req.endYear,
        compouding_periods                  = req.compoundingPeriods,
        fourohone_k_starting_amount         = req.fourOhOneKStartingAmount,
        fourohone_k_monthly_contributions   = req.fourOhOneKMonthlyContributions,
        roth_ira_starting_amount            = req.rothIraStartingAmount,
        roth_ira_monthly_contributions      = req.rothIraMonthlyContributions,
        brokerage_starting_amount           = req.brokerageStartingAmount,
        brokerage_monthly_contributions     = req.brokerageMonthlyContributions,
        as_json                             = True)

@router.post("/number/simple")
async def number_simple_async(req: NumberSimpleRequest):
    return retirement.number_simple(current_salary = req.currentSalary)

@router.post("/number")
async def number_async(req: NumberRequest):
    return retirement.number(
        desired_retirement_age  = req.desiredRetirementAge,
        desired_monthly_income  = req.desiredMonthlyIncome,
        retirement_end_age      = req.retirementEndAge)