from pydantic import BaseModel
from typing import Optional


# Assets
# Include anything purchased with cash or with a loan – car, house, boat, investment property, etc. 
# Mainly interested in larger purchases (i.e., don’t care if financing a microwave)


class Asset:
    _types = [
        "car",
        "house",
        "boat",
        "stock",
        "investment property",
        "cash",
        "other"
    ]

    def __init__(self, name, type, value):
        self.name = name
        self.type = type if type in self._types else "other"
        self.value = value


class ComparableAsset(BaseModel):
    name: Optional[str]
    type: Optional[str]
    value: float

    interest: Optional[float] = 8                               # Interest
    hysInterest: Optional[float] = 1.75                         # High yield savings interest
    years: Optional[int] = 25                                   # Number of years to compound
    frequency: Optional[int] = 12                               # Frequency of compounding, 12 = monthly
    investmentFees: Optional[float] = 0                         # Investment fees, if any   (reduced from interest)
    taxDrag: Optional[float] = 0                                # Tax drag, if any          (reduced from interest)
    contribution: Optional[float] = 500                         # Contribution per frequency

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
