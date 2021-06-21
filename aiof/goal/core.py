import datetime
from numpy import promote_types
import pandas as pd
import numpy_financial as npf

from typing import List

import aiof.config as config

from aiof.data.goal import Goal, GoalTrip
from aiof.data.asset import Asset
from aiof.data.liability import Liability


# Configs
_settings = config.get_settings()
_default_interest = _settings.DefaultInterest
_round_dig = _settings.DefaultRoundingDigit


def analyze(
    goal: Goal,
    monthly_income: float,
    current_goals: List[Goal],
    current_assets: List[Asset],
    current_liabilities: List[Liability],
    as_json = False) -> pd.DataFrame:
    """
    Analyze goal

    Parameters
    ----------
    """
    total_asset_value = sum(a.value if a.value is not None else 0 for a in current_assets)
    total_liability_value = sum(l.value if l.value is not None else 0 for l in current_liabilities)
    total_liability_monthly_payment = sum(l.monthlyPayment if l.monthlyPayment is not None else 0 for l in current_liabilities)

    income_liability_diff = monthly_income - total_liability_monthly_payment

    asset_type = _settings.AssetType
    goal_type = _settings.GoalType

    # Your monthly income is bigger than your liability spending
    #   this means that you have spare income to potentially cover the goal
    df = pd.DataFrame()
    if income_liability_diff > 0:
        if income_liability_diff < goal.monthlyContribution:
            return df
        else:
            total_asset_cash = sum(a.value for a in [a for a in current_assets if a.typeName.lower() in asset_type.CASH and a.value is not None])
            total_goal_monthly_contribution = sum(g.monthlyContribution for g in current_goals)

            df = pd.DataFrame(columns=["year", "goal"])

            for i in range(1, 6):
                df.loc[i, "year"] = i
                df.loc[i, "goal"] = -npf.fv(
                    rate=0.07/12,
                    nper=12,
                    pmt=goal.monthlyContribution,
                    pv=goal.amount)
                    
    df = df.round(_round_dig)
    return df if not as_json else df.to_dict(orient="records")