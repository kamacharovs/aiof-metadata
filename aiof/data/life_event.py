import datetime

from pydantic import BaseModel, validator
from typing import Optional


_event_types = [
    "having a child",
    "buying a car",
    "selling a car",
    "buying a house",
    "buying a condo",
]

class LifeEvent(BaseModel):
    """
    Life event class. This is used to generate a life event
    """
    type: str
    amount: float
    plannedDate: Optional[datetime.datetime]

    @validator("type")
    def type_must_be_valid(cls, t):
        if t not in _event_types:
            raise ValueError("Invalid type. Please use one of the following {0}".format(", ".join(str(x) for x in _event_types)))
        return t.title()
