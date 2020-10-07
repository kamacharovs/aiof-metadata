from pydantic import BaseModel
from typing import Optional, List

from aiof.data.asset import Asset
from aiof.data.liability import Liability


class Analytics(BaseModel):
    diff: Optional[float]
    cashToCcRation: Optional[float]
    ccToCashRatio: Optional[float]


class AssetsLiabilitiesRequest(BaseModel):
    assets: List[Asset]
    liabilities: List[Liability]

class AssetsLiabilities(BaseModel):
    assets: List[float]
    liabilities: List[float]

    assetsTotal: float
    assetsMean: float

    liabilitiesTotal: float
    liabilitiesMean: float

    analytics: Analytics
