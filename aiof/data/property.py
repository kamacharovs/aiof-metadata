import datetime

from pydantic import BaseModel
from typing import Optional


class MortgageCalculatorRequest(BaseModel):
    propertyValue: Optional[float]
    downPayment: Optional[float]
    interestRate: Optional[float]
    loanTermYears: Optional[int]
    startDate: Optional[datetime.datetime]
    pmi: Optional[float]
    propertyInsurance: Optional[float]
    monthlyHoa: Optional[float]