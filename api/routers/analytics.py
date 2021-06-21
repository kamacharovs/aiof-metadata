import aiof.analytics.core as a

from aiof.data.analytics import AssetsLiabilitiesRequest
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