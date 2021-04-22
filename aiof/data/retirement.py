from pydantic import BaseModel
from typing import Optional


class WithdrawalRequest(BaseModel):
    retirementNumber: float
    takeOutPercentage: float
    numberOfYears: float

class CommonInvestmentsRequest(BaseModel):
    interest: Optional[float]
    startYear: Optional[int]
    endYear: Optional[int]
    compoundingPeriods: Optional[int]
    fourOhOneKStartingAmount: Optional[float]
    fourOhOneKMonthlyContributions: Optional[float]
    rothIraStartingAmount: Optional[float]
    rothIraMonthlyContributions: Optional[float]
    brokerageStartingAmount: Optional[float]
    brokerageMonthlyContributions: Optional[float]

class NumberSimpleRequest(BaseModel):
    currentSalary: Optional[float]

class NumberRequest(BaseModel):
    desiredRetirementAge:   Optional[int]
    desiredMonthlyIncome:   Optional[float]
    retirementEndAge:       Optional[int]