import math
import datetime

import aiof.config as config

from aiof.data.fi import CoastFireSavings

from typing import List

# Configs
_settings = config.get_settings()
_round_dig = _settings.DefaultRoundingDigit


def coast_fire_savings(
    initial_interest_rate: float = 2,
    start_age: int = 30,
    end_age: int = 90,
    current_balance: float = 100000,
    coast_savings: List[CoastFireSavings] = None) -> List[CoastFireSavings]:
    """
    Show how savings will be affected for Coast FIRE

    Parameters
    ----------
    `initial_interest_rate` : float.
        initial interest amount used. defaults to `2`\n
    `start_age` : float.
        initial interest amount used. defaults to `2`\n

    Notes
    ----------
    Based on https://www.reddit.com/r/financialindependence/comments/ja3nks/i_built_a_coastfire_compatible_savings_sheet/
    """
    year = datetime.datetime.now().year
    percentage_to_flip_interest = 0.3
    years_to_flip_interest = math.ceil(end_age - (end_age * percentage_to_flip_interest))

    # If coast_savings is None, then generate it
    if coast_savings is None:
        coast_savings = list(CoastFireSavings)

        for i in range(start_age, end_age, 1):
            yearly_return = 0.08 if i < years_to_flip_interest else 0.06

            coast_savings = CoastFireSavings(
                age=i,
                year=year,
                yearlyReturn=yearly_return
            )
            coast_savings.append(coast_savings)
            year += 1
