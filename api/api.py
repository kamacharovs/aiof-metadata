import os
import aiof.config as config
import aiof.helpers as helpers
import aiof.fi.core as fi

from aiof.data.fi import *
from aiof.data.asset import ComparableAsset

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from functools import lru_cache


app = FastAPI()


@lru_cache()
def settings():
    return config.Settings()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings().cors_origins,
    allow_credentials=True,
    allow_methods=settings().cors_allowed_methods,
    allow_headers=settings().cors_allowed_headers,
)


# FI
@app.post("/api/fi/time")
async def time_to_fi(req: FiTime):
    return fi.time_to_fi(req.startingAmount,
        req.monthlyInvestment,
        req.desiredYearsExpensesForFi,
        req.desiredAnnualSpending)

@app.post("/api/fi/rule/of/72")
async def rule_of_72(req: FiRuleOf72):
    return fi.rule_of_72(req.startingAmount,
        req.interest)

@app.post("/api/fi/added/time")
async def added_time(req: FiAddedTime):
    return fi.added_time_to_fi(req.monthlyInvestment,
        req.totalAdditionalExpense)

@app.get("/api/fi/ten/million/dream/{monthlyInvestment}")
async def ten_million_dream(monthlyInvestment: float):
    return fi.ten_million_dream(monthlyInvestment)

@app.post("/api/fi/compound/interest")
async def compound_interest(req: FiCompoundInterest):
    return fi.compound_interest(req.startingAmount,
        req.monthlyInvestment,
        req.interest,
        req.numberOfYears,
        req.investmentFees,
        req.taxDrag)

@app.post("/api/fi/investment/fees/effect")
async def investment_fees_effect(req: FiInvestmentFeesEffect):
    return fi.investment_fees_effect(req.ageAtCareerStart,
        req.interestReturnWhileWorking,
        req.interestReturnWhileRetired,
        req.taxDrag,
        req.annualSavingsFirstDecade,
        req.annualSavingsSecondDecade,
        req.annualWithdrawalThirdDecade)

@app.post("/api/fi/cost/of/raising/children")
async def cost_of_raising_children(req: FiRaisingChildren):
    return fi.cost_of_raising_children(req.annualExpensesStart,
        req.annualExpensesIncrement,
        req.children,
        req.interests)
@app.get("/api/fi/cost/of/raising/children/families")
async def cost_of_raising_children_families():
    return fi.cost_of_raising_children_faimilies()

@app.post("/api/fi/savings/rate")
async def savings_rate(req: SavingsRate):
    return fi.savings_rate(req.salary,
        req.matchAndProfitSharing,
        req.federalIncomeTax,
        req.stateIncomeTax,
        req.fica,
        req.healthAndDentalInsurance,
        req.otherDeductibleBenefits,
        req.hsaInvestment,
        req.fourOhOneKOrFourOhThreeB,
        req.fourFiveSevenB,
        req.sepIra,
        req.otherTaxDeferred,
        req.rothIra,
        req.taxableAccount,
        req.education,
        req.mortgagePrincipal,
        req.studentLoanPrincipal,
        req.otherPostTaxInvestment,
        req.currentNestEgg)

@app.get("/api/export/to/csv")
async def export_to_csv():
    return fi.export_to_csv(fi.rule_of_72(100000, 7))


@app.post("/api/asset/breakdown")
async def asset_breakdown(asset: ComparableAsset):
    return helpers.asset_breakdown(asset)

@app.get("/api/asset/breakdown/csv")
async def export_asset_fv_breakdown_as_table_to_csv():
    df = helpers.asset_fv_breakdown_as_table(
        asset_value=15957,
        contribution=500,
        years=15,
        rate=(8/100)/12,
        frequency=12,
    )
    response = StreamingResponse(helpers.export_to_csv(df),
                                media_type="text/csv")
    return response 


@app.get("/api/frequencies")
async def frequencies():
    return helpers._frequency


@app.get("/api/app/settings")
async def info(settings: config.Settings = Depends(settings)):
    return {
        "aiof_portal_url": settings.aiof_portal_url,
    }