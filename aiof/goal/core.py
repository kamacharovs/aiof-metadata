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
    monthly_income: float,
    current_goals: List[Goal],
    current_assets: List[Asset],
    current_liabilities: List[Liability]
    ) -> pd.DataFrame:
    """
    Analyze goal

    Parameters
    ----------
    """
    total_asset_value = sum(a.value if a.value is not None else 0 for a in current_assets)
    total_liability_value = sum(l.value if l.value is not None else 0 for l in current_liabilities)
    total_liability_monthly_payment = sum(l.monthlyPayment if l.monthlyPayment is not None else 0 for l in current_liabilities)

    income_liability_diff = monthly_income - total_liability_monthly_payment

    asset_type = config.get_settings().AssetType
    goal_type = config.get_settings().GoalType

    if income_liability_diff < 0:
        total_asset_cash = sum(a.value for a in [a for a in current_assets if a.typeName.lower() in asset_type.CASH and a.value is not None])
        