import datetime

from aiof.data.asset import Asset
from aiof.data.liability import Liability

from pydantic import BaseModel, validator
from typing import List, Optional


_event_types = [
    "having a child",
    "buying a car",
    "selling a car",
    "buying a house",
    "buying a condo",
]

class LifeEventRequest(BaseModel):
    """
    Life event request class. This is used to request specific event
    """
    assets: List[Asset]
    liabilities: Optional[List[Liability]]
    type: str
    amount: float
    plannedDate: Optional[datetime.datetime]

    @validator("type")
    def type_must_be_valid(cls, t):
        if t not in _event_types:
            raise ValueError("Invalid type. Please use one of the following {0}".format(", ".join(str(x) for x in _event_types)))
        return t.title()


class LifeEventResponse(BaseModel):
    """
    Life event response class. This is used to return specific response
    """
    currentAssets: List[Asset]
    currentLiabilities: List[Liability] 
