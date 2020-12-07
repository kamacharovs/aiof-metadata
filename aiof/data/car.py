from pydantic import BaseModel
from typing import Optional


# Car
# Anything and everything car related models


class CarLoanRequest(BaseModel):
    carLoan: Optional[float]
    interst: Optional[float]
    years: Optional[int]
