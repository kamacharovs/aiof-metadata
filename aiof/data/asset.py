from datetime import datetime

from pydantic import BaseModel
from typing import Optional, List


# Assets
# Include anything purchased with cash or with a loan – car, house, boat, investment property, etc. 
# Mainly interested in larger purchases (i.e., don’t care if financing a microwave)

_default_interest = 8
_default_hysInterest = 1.75
_default_years = 25
_default_frequency = 12
_default_investmentFees = 0
_default_taxDrag = 0
_default_contribution = 500


class AssetSnapshot(BaseModel):
    assetId: int
    name: Optional[str]
    typeName: Optional[str]
    value: Optional[float]
    valueChange: Optional[float]
    created: datetime

class Asset(BaseModel):
    name: Optional[str]
    typeName: str
    value: float

    snapshots: Optional[List[AssetSnapshot]]

    def subtract(self, value):
        self.value - value
    def add(self, value):
        self.value + value

class AssetFv(BaseModel):
    year: Optional[int]
    typeName: Optional[str]
    interest: Optional[float]
    pv: Optional[float]
    fv: Optional[float]


class ComparableAsset(BaseModel):
    name: Optional[str]
    typeName: Optional[str]
    value: float

    interest: Optional[float] = _default_interest               # Interest
    hysInterest: Optional[float] = _default_hysInterest         # High yield savings interest
    years: Optional[int] = _default_years                       # Number of years to compound
    frequency: Optional[int] = _default_frequency               # Frequency of compounding, 12 = monthly
    investmentFees: Optional[float] = _default_investmentFees   # Investment fees, if any   (reduced from interest)
    taxDrag: Optional[float] = _default_taxDrag                 # Tax drag, if any          (reduced from interest)
    contribution: Optional[float] = _default_contribution       # Contribution per frequency

    marketValue: Optional[float] = None                         # What if asset's value is invested in the market at [interest]% return?
    marketBeginValue: Optional[float] = None                       # When the compounding is at the beginning
    marketValueBreakdown: Optional[list] = None                    # Breakdown of each year

    marketWithContributionValue: Optional[float] = None         # What if asset's value is invested in the market at [interest]% return with monthly contributions?
    marketBeginWithContributionValue: Optional[float] = None        # When the compounding is at the beginning
    marketWithContributionValueBreakdown: Optional[list] = None     # Breakdown of each year

    hysValue: Optional[float] = None                            # What if asset's value is put in a High Yield Savings Account at 1.75% interest?
    hysBeginValue: Optional[float] = None                           # When the compounding is at the beginning
    hysValueBreakdown: Optional[list] = None                        # Breakdown of each year

    hysWithContributionValue: Optional[float] = None            # What if asset's value is put in a High Yield Savings Account at 1.75% interest with monthly contributions?
    hysBeginWithContributionValue: Optional[float] = None           # When the compounding is at the beginning
    hysWithContributionValueBreakdown: Optional[list] = None        # Breakdown of each year

    def init_values(self):
        self.interest = self.interest if self.interest is not None else _default_interest
        self.hysInterest = self.hysInterest if self.hysInterest is not None else _default_hysInterest
        self.years = self.years if self.years is not None else _default_years
        self.frequency = self.frequency if self.frequency is not None else _default_frequency
        self.investmentFees = self.investmentFees if self.investmentFees is not None else _default_investmentFees
        self.taxDrag = self.taxDrag if self.taxDrag is not None else _default_taxDrag
        self.contribution = self.contribution if self.contribution is not None else _default_contribution
