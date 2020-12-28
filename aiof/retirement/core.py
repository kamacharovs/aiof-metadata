import datetime
from numpy.lib.financial import pmt
import pandas as pd
import numpy_financial as npf

import aiof.config as config

from aiof.helpers import fv


# Configs
_settings = config.get_settings()
_default_interest = _settings.DefaultInterest
_round_dig = _settings.DefaultRoundingDigit


def withdrawal_calc(
    retirement_number: float = None,
    take_out_percentage: float = None,
    number_of_years: int = None,
    as_json: bool = False) -> pd.DataFrame:
    """
    Calculate retirement

    Parameters
    ----------
    `retirement_number` : float.
        retirement number. defaults to `1,000,000`\n
    `take_out_percentage` : float.
        take out percentage of total retirement number. defaults to `3%`\n
    `number_of_years` : int.
        number of years to take money out. defaults to `35`
    """
    # Check for None
    retirement_number   = retirement_number if retirement_number is not None else 1000000
    take_out_percentage = take_out_percentage if take_out_percentage is not None else 3
    number_of_years     = number_of_years if number_of_years is not None else 35

    # Check and fix parameters
    take_out_percentage = take_out_percentage / 100

    if retirement_number <= 0:
        raise ValueError("Retirement number cannot be negative")
    elif take_out_percentage <= 0 or take_out_percentage > 0.1:
        raise ValueError("Take out percentage must be between 1 and 100")
    elif number_of_years <= 0 or number_of_years > 100:
        raise ValueError("Number of years must be between 1 and 100")

    # Initial data frame
    df = pd.DataFrame(columns=["year", "takeOutPercentage", "startingRetirementNumber", "withdrawal", "endingRetirementNumber"], dtype="float")

    withdrawal = retirement_number * take_out_percentage

    df.loc[0, "year"] = 1
    df.loc[0, "takeOutPercentage"] = take_out_percentage
    df.loc[0, "startingRetirementNumber"] = retirement_number
    df.loc[0, "withdrawal"] = withdrawal
    df.loc[0, "endingRetirementNumber"] =-npf.fv(
            rate=_default_interest / 100,
            nper=1,
            pmt=0,
            pv=retirement_number - withdrawal,
            when='end')

    if take_out_percentage == 100:
        return df if not as_json else df.to_dict(orient="records")

    for year in range(1, int(number_of_years)):
        df.loc[year, "year"] = year + 1
        df.loc[year, "takeOutPercentage"] = take_out_percentage
        df.loc[year, "startingRetirementNumber"] = df.loc[year - 1, "endingRetirementNumber"]
        df.loc[year, "withdrawal"] = withdrawal
        df.loc[year, "endingRetirementNumber"] = -npf.fv(
            rate=_default_interest / 100,
            nper=1,
            pmt=0,
            pv=df.loc[year, "startingRetirementNumber"] - df.loc[year, "withdrawal"],
            when='end')
    df["year"] = df["year"].astype(int)
    df = df.round(_round_dig)

    return df if not as_json else df.to_dict(orient="records")