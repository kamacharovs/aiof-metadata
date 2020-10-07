import aiof.analytics.core as a

from aiof.data.analytics import AssetsLiabilitiesRequest

from fastapi import APIRouter


router = APIRouter()


@router.post("/analyze", tags=["car"])
async def analyze(req: AssetsLiabilitiesRequest):
    return a.analyze(
        assets=req.assets,
        liabilities=req.liabilities)