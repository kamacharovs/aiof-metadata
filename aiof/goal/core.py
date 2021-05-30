import datetime
import pandas as pd
import numpy_financial as npf

from typing import List

import aiof.config as config

from aiof.data.goal import Goal, GoalTrip


def analyze(
    goal: Goal,
    current_goals: List[Goal]
    ) -> pd.DataFrame:
    """
    Analyze goal

    Parameters
    ----------
    """