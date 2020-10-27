from pydantic import BaseModel
from typing import Optional


# Anything that you are paying interest on:
#   - Credit card
#   - Student loans
#   - Car loan
#   - Mortgage
#   - House renovation
#   - RV
#   - Any personal loan
#   - Etc.

class Liability(BaseModel):
    name: str
    type: str
    value: float

    years: Optional[int]
    monthlyPayment: Optional[float]