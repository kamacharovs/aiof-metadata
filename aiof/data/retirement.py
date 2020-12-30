import datetime

from pydantic import BaseModel
from typing import Optional


class WithdrawalRequest(BaseModel):
    retirementNumber: float
    takeOutPercentage: float
    numberOfYears: float