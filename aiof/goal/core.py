import datetime
import pandas as pd
import numpy_financial as npf

from typing import List

import aiof.config as config

from aiof.data.goal import Goal, GoalTrip
from aiof.data.asset import Asset
from aiof.data.liability import Liability


def analyze(
    goal: Goal,
    current_goals: List[Goal],
    current_assets: List[Asset],
    current_liabilities: List[Liability]
    ) -> pd.DataFrame:
    """
    Analyze goal

    Parameters
    ----------
    """