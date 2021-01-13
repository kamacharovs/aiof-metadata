from pydantic import BaseModel
from typing import Optional


# Car
# Anything and everything car related models


class CarLoanRequest(BaseModel):
    carLoan: Optional[float]
    interst: Optional[float]
    years: Optional[int]

class CarLoanResponse(BaseModel):
    carLoan: float
    interest: float
    years: int
    monthlyPayment: float
    data: object

    class Config:
        arbitrary_types_allowed = True


class CarValueDepreciationRequest(BaseModel):
    value: Optional[float]
    years: Optional[int]
