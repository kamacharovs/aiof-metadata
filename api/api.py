import os
import aiof.config as config
import aiof.helpers as helpers
import aiof.fi.core as fi

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from functools import lru_cache


class FiTime(BaseModel):
    startingAmount: Optional[float] = None
    monthlyInvestment: Optional[float] = None
    desiredYearsExpensesForFi: Optional[int] = None
    desiredAnnualSpending: Optional[float] = None

class FiRuleOf72(BaseModel):
    startingAmount: Optional[float] = None
    interest: Optional[float] = None

class FiAddedTime(BaseModel):
    monthlyInvestment: Optional[float] = None
    totalAdditionalExpense: Optional[float] = None

class FiCompoundInterest(BaseModel):
    startingAmount: Optional[float] = None
    monthlyInvestment: Optional[float] = None
    interest: Optional[float] = None
    numberOfYears: Optional[int] = None
    investmentFees: Optional[float] = None
    taxDrag: Optional[float] = None

class FiInvestmentFeesEffect(BaseModel):
    ageAtCareerStart: Optional[int] = None
    interestReturnWhileWorking: Optional[float] = None
    interestReturnWhileRetired: Optional[float] = None
    taxDrag: Optional[float] = None
    annualSavingsFirstDecade: Optional[float] = None
    annualSavingsSecondDecade: Optional[float] = None
    annualWithdrawalThirdDecade: Optional[float] = None

class FiRaisingChildren(BaseModel):
    annualExpensesStart: Optional[float] = None
    annualExpensesIncrement: Optional[float] = None
    children: Optional[list] = None
    interests: Optional[list] = None


app = FastAPI()

origins = [
    "http://localhost:4100",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache()
def get_settings():
    return config.Settings()


# FI
@app.post("/api/fi/time")
def time_to_fi(req: FiTime):
    return fi.time_to_fi(req.startingAmount,
        req.monthlyInvestment,
        req.desiredYearsExpensesForFi,
        req.desiredAnnualSpending)

@app.post("/api/fi/rule/of/72")
def rule_of_72(req: FiRuleOf72):
    return fi.rule_of_72(req.startingAmount,
        req.interest)

@app.post("/api/fi/added/time")
def added_time(req: FiAddedTime):
    return fi.added_time_to_fi(req.monthlyInvestment,
        req.totalAdditionalExpense)

@app.get("/api/fi/ten/million/dream/{monthlyInvestment}")
def ten_million_dream(monthlyInvestment: float):
    return fi.ten_million_dream(monthlyInvestment)

@app.post("/api/fi/compound/interest")
def compound_interest(req: FiCompoundInterest):
    return fi.compound_interest(req.startingAmount,
        req.monthlyInvestment,
        req.interest,
        req.numberOfYears,
        req.investmentFees,
        req.taxDrag)

@app.post("/api/fi/investment/fees/effect")
def investment_fees_effect(req: FiInvestmentFeesEffect):
    return fi.investment_fees_effect(req.ageAtCareerStart,
        req.interestReturnWhileWorking,
        req.interestReturnWhileRetired,
        req.taxDrag,
        req.annualSavingsFirstDecade,
        req.annualSavingsSecondDecade,
        req.annualWithdrawalThirdDecade)

@app.post("/api/fi/cost/of/raising/children")
def cost_of_raising_children(req: FiRaisingChildren):
    return fi.cost_of_raising_children(req.annualExpensesStart,
        req.annualExpensesIncrement,
        req.children,
        req.interests)
@app.get("/api/fi/cost/of/raising/children/families")
def cost_of_raising_children_families():
    return fi.cost_of_raising_children_faimilies()


@app.get("/api/frequencies")
def frequencies():
    return helpers._frequency


@app.get("/app/settings")
async def info(settings: config.Settings = Depends(get_settings)):
    return {
        "aiof_portal_url": settings.aiof_portal_url,
    }