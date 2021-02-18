import datetime
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

    if take_out_percentage == 0.1:
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


def common_investments(
    interest: float,
    start_year: int,
    end_year: int,
    compouding_periods: int,
    fourohone_k_starting_amount: float = None,
    fourohone_k_monthly_contributions: float = None,
    roth_ira_starting_amount: float = None,
    roth_ira_monthly_contributions: float = None,
    brokerage_starting_amount: float = None,
    brokerage_monthly_contributions: float = None,
    as_json: bool = False) -> pd.DataFrame:
    """
    Calculate common retirement investments - 401(k), Roth IRA, Brokerage

    Parameters
    ----------
    `as_json` : bool.
        whether to return the data as JSON. defaults to `False`
    """
    # Check for None
    interest = interest if interest is not None else 7
    start_year = start_year if start_year is not None else datetime.datetime.today().year
    end_year = end_year if end_year is not None else start_year + 10
    compouding_periods = compouding_periods if compouding_periods is not None else 12
    fourohone_k_starting_amount = fourohone_k_starting_amount if fourohone_k_starting_amount is not None else 0
    fourohone_k_monthly_contributions = fourohone_k_monthly_contributions if fourohone_k_monthly_contributions is not None else 500
    roth_ira_starting_amount = roth_ira_starting_amount if roth_ira_starting_amount is not None else 0
    roth_ira_monthly_contributions = roth_ira_monthly_contributions if roth_ira_monthly_contributions is not None else 500
    brokerage_starting_amount = brokerage_starting_amount if brokerage_starting_amount is not None else 0
    brokerage_monthly_contributions = brokerage_monthly_contributions if brokerage_monthly_contributions is not None else 500

    # Check and fix parameters
    if (interest > 100 or interest < 1):
        raise ValueError("Interest must be at least 1% and less than or equal to 100%")
    elif (end_year <= start_year):
        raise ValueError("Start year cannot be less than end year")
    elif (fourohone_k_starting_amount < 0):
        raise ValueError("401(k) starting amount cannot be less than 0")
    elif (fourohone_k_monthly_contributions < 0):
        raise ValueError("401(k) monthly contributions cannot be less than 0")
    elif (roth_ira_starting_amount < 0):
        raise ValueError("Roth IRA starting amount cannot be less than 0")
    elif (roth_ira_monthly_contributions < 0):
        raise ValueError("Roth IRA monthly contributions cannot be less than 0")
    elif (brokerage_starting_amount < 0):
        raise ValueError("Brokerage starting amount cannot be less than 0")
    elif (brokerage_monthly_contributions < 0):
        raise ValueError("Brokerage monthly contributions cannot be less than 0")

    interest = interest / 100

    # Initial data frame
    df = pd.DataFrame(columns=["year", "compoundingPeriods", "fourohoneK", "fourohoneKMonthlyContributions", "rothIra", "rothIraMonthlyContributions", "brokerage", "brokerageMonthlyContributions"], dtype="float")

    df.loc[0, "year"] = start_year
    df.loc[0, "compoundingPeriods"] = compouding_periods
    df.loc[0, "fourohoneK"] = fourohone_k_starting_amount
    df.loc[0, "fourohoneKMonthlyContributions"] = fourohone_k_monthly_contributions
    df.loc[0, "rothIra"] = fourohone_k_starting_amount
    df.loc[0, "rothIraMonthlyContributions"] = roth_ira_monthly_contributions
    df.loc[0, "brokerage"] = brokerage_starting_amount
    df.loc[0, "brokerageMonthlyContributions"] = brokerage_monthly_contributions

    for i in range(1, int(end_year - start_year) + 1):
        df.loc[i, "year"] = start_year + i
        df.loc[i, "compoundingPeriods"] = compouding_periods

    df["year"] = df["year"].astype(int)
    df = df.round(_round_dig)

    print(df)