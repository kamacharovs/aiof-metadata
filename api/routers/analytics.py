import aiof.analytics.core as a

from aiof.data.analytics import AssetsLiabilitiesRequest
from aiof.data.life_event import LifeEventRequest

from fastapi import APIRouter


router = APIRouter()


@router.post("/analyze")
async def analyze(req: AssetsLiabilitiesRequest):
    return a.analyze(
        assets      = req.assets,
        liabilities = req.liabilities)

@router.post("/life/event")
async def analyze(req: LifeEventRequest):
    return a.life_event(req = req)