import aiof.analytics.core as a

from aiof.data.asset import Asset
from aiof.data.liability import Liability

from fastapi import APIRouter


router = APIRouter()


@router.post("/analyze", tags=["car"])
async def analyze():
    return a.analyze(
        [
            Asset(name="asset 1", type="cash", value=35000),
            Asset(name="asset 2", type="cash", value=8000),
            Asset(name="asset 3", type="stock", value=24999)
        ],
        [
            Liability(name="liabiliy 1", type="credit card", value=15000),
            Liability(name="liabiliy 2", type="credit card", value=2564),
            Liability(name="liabiliy 3", type="personal loan", value=4999)
        ]
    )