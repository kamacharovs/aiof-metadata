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