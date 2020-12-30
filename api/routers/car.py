import aiof.car.core as car

from aiof.data.car import CarLoanRequest

from fastapi import APIRouter


router = APIRouter()


@router.post("/loan")
async def car_loan(req: CarLoanRequest):
    return car.loan_calc(
        car_loan        = req.carLoan,
        interest        = req.interst,
        years           = req.years,
        data_as_json    = True)