import aiof.car.core as car

from aiof.data.car import CarLoanRequest, CarValueDepreciationRequest

from fastapi import APIRouter


router = APIRouter()


@router.post("/loan")
async def car_loan(req: CarLoanRequest):
    return car.loan_calc(
        car_loan        = req.carLoan,
        interest        = req.interst,
        years           = req.years,
        data_as_json    = True)

@router.post("/depreciation")
async def value_depreciation(req: CarValueDepreciationRequest):
    return car.value_depreciation_calc(
        loan_amount = req.value,
        years       = req.years,
        as_json     = True)