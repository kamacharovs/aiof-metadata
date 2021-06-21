import aiof.analytics.core as a

from aiof.data.analytics import AssetsLiabilitiesRequest, DebtToIncomeRatioRequest
from aiof.data.life_event import LifeEventRequest

from fastapi import APIRouter


router = APIRouter()


@router.post("/analyze")
async def analyze(req: AssetsLiabilitiesRequest):
    return a.analyze(
        assets          = req.assets,
        liabilities     = req.liabilities,
        annual_income   = req.annualIncome)

@router.get("/life/event/types")
async def get_life_event_types():
    return a.life_event_types()


@router.post("/life/event")
async def get_life_event(req: LifeEventRequest):
    return a.life_event(
        req     = req,
        as_json = True)


@router.post("/debt/income/ratio")
async def debt_to_income_ratio(req: DebtToIncomeRatioRequest):
    return a.debt_to_income_ratio_calc(
        annual_income   = req.annualIncome,
        liabilities     = req.liabilities)