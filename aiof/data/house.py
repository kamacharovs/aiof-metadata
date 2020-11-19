from pydantic import BaseModel
from typing import Optional


class MortgageCalculatorBreakdown(BaseModel):
    totalMonthlyPayment: float
    downPayment: float