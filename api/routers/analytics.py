import aiof.analytics.core as a

from aiof.data.asset import Asset
from aiof.data.liability import Liability

from fastapi import APIRouter


router = APIRouter()


@router.post("/analyze", tags=["car"])
async def analyze():
    return a.analyze(
        [
            Asset(name="test", type="test", value=35000),
            Asset(name="asset 1", type="asset 2", value=8000)
        ],
        [
            Liability(name="test", type="test", value=15000),
            Liability(name="test 2", type="test 2", value=2564)
        ]
    )