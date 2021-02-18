import datetime

from pydantic import BaseModel
from typing import Optional


class WithdrawalRequest(BaseModel):
    retirementNumber: float
    takeOutPercentage: float
    numberOfYears: float

class CommonInvestmentsRequest(BaseModel):
    interest: float
    startYear: int
    endYear: int
    compoundingPeriods: int
    fourOhOneKStartingAmount: float
    fourOhOneKMonthlyContributions: float
    rothIraStartingAmount: float
    rothIraMonthlyContributions: float
    brokerageStartingAmount: float
    brokerageMonthlyContributions: float