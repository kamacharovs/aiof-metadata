from pydantic import BaseModel
from typing import Optional

from aiof.data.asset import Asset
from aiof.data.liability import Liability


class AssetsLiabilities(BaseModel):
    assets: list
    liabilities: list

    assetsTotal: float
    assetsMean: float

    liabilitiesTotal: float
    liabilitiesMean: float

    analytics: dict
