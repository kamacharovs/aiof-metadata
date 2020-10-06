import aiof.analytics.core as a
from aiof.data.liability import Liability

from fastapi import APIRouter


router = APIRouter()


@router.get("/analyze", tags=["car"])
async def analyze():
    return a.analyze(
        None,
        [
            Liability(name="test", type="test", value=15000),
            Liability(name="test 2", type="test 2", value=2564)
        ]
    )