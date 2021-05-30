from datetime import datetime

from pydantic import BaseModel
from typing import Optional, List

from aiof.data.asset import Asset
from aiof.data.liability import Liability


# Financial Goals
#   - Mandatory short-term goals
class Goal(BaseModel):
    name: str
    type: str
    amount: Optional[float]
    currentAmount: Optional[float]
    monthlyContribution: Optional[float]
    plannedDate: datetime
    projectedDate: Optional[datetime]

class GoalTrip(Goal):
    destination: str
    tripType: str
    Duration: float
    travelers: int
    flight: Optional[float]
    hotel: Optional[float]
    car: Optional[float]
    food: Optional[float]
    activities: Optional[float]
    other: Optional[float]

class GoalAnalyzeRequest(BaseModel):
    goal: Goal
    currentGoals: List[Goal]
    currentAssets: List[Asset]
    currentLiabilities: List[Liability]