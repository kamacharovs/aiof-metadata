import aiof.retirement.core as retirement

from aiof.data.retirement import WithdrawalRequest

from fastapi import APIRouter


router = APIRouter()


@router.post("/withdrawal")
async def withdrawal_calc(req: WithdrawalRequest):
    return retirement.withdrawal_calc(
        retirement_number   = req.retirementNumber,
        take_out_percentage = req.takeOutPercentage,
        number_of_years     = req.numberOfYears,
        as_json             = True)

@router.post("/common/investments")
async def common_investments():
    return retirement.common_investments(
        interest=7,
        start_year=2020,
        end_year=2050,
        compouding_periods=12,
        fourohone_k_starting_amount=1000,
        fourohone_k_monthly_contributions=1625,
        roth_ira_starting_amount=1000,
        roth_ira_monthly_contributions=500,
        brokerage_starting_amount=1000,
        brokerage_monthly_contributions=500)