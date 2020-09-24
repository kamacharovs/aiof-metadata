import os
import aiof.fi.core as fi

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


class FiTime(BaseModel):
    startingAmount: Optional[float] = None
    monthlyInvestment: Optional[float] = None
    desiredYearsExpensesForFi: Optional[int] = None
    desiredAnnualSpending: Optional[float] = None


app = FastAPI()


# FI
@app.post("/metadata/fi/time/to/fi")
def time_to_fi(req: FiTime):
    return fi.time_to_fi(req.startingAmount,
        req.monthlyInvestment,
        req.desiredYearsExpensesForFi,
        req.desiredAnnualSpending)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
