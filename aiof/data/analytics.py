from pydantic import BaseModel
from typing import Optional, List

from aiof.data.asset import Asset, AssetFv
from aiof.data.liability import Liability


class Analytics(BaseModel):
    diff: Optional[float] = None
    cashToCcRatio: Optional[float] = None
    ccToCashRatio: Optional[float] = None
    debtToIncomeRatio: Optional[float] = None
    assetsFv: Optional[List[AssetFv]] = None


class AssetsLiabilitiesRequest(BaseModel):
    assets: List[Asset]
    liabilities: List[Liability]
    annualIncome: float

class AssetsLiabilities(BaseModel):
    assets: List[float]
    liabilities: List[float]

    assetsTotal: float
    assetsMean: float

    liabilitiesTotal: float
    liabilitiesMean: float

    analytics: Analytics


class DebtToIncomeRatioRequest(BaseModel):
    annualIncome: float
    liabilities: List[Liability]