import datetime
import pandas as pd
import numpy_financial as npf

import aiof.config as config


# Configs
_settings = config.get_settings()
_round_dig = _settings.DefaultRoundingDigit


def withdrawal_calc(
    retirement_number: float = None,
    take_out_percentage: float = None,
    number_of_years: float = None,
    as_json: bool = False) -> pd.DataFrame:
    """
    Calculate retirement

    Parameters
    ----------
    `retirement_number` : float.
        retirement number. defaults to `1,000,000`\n
    `take_out_percentage` : float.
        take out percentage of total retirement number. defaults to `3%`\n
    `number_of_years` : float.
        number of years to take money out. defaults to `35`
    """
    # Check for None
    retirement_number   = retirement_number if retirement_number is not None else 1000000
    take_out_percentage = take_out_percentage if take_out_percentage is not None else 3
    number_of_years     = number_of_years if number_of_years is not None else 35

    # Check and fix parameters
    take_out_percentage = take_out_percentage / 100

    if retirement_number < 0:
        raise ValueError("Retirement number cannot be negative")
    elif take_out_percentage < 0 or take_out_percentage > 100:
        raise ValueError("Take out percentage must be between 0 and 100")
    elif number_of_years < 0 or number_of_years > 100:
        raise ValueError("Number of years must be between 0 and 100")

    # Initial data frame
    df = pd.DataFrame(columns=["year", "principalPaid", "interestPaid", "startingBalance", "endingBalance"], dtype="float")
    df.reset_index(inplace=True)
    df.index += 1
    df.index.name = "period"

    print(df)