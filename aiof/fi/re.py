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
        coast_savings = []
        contribution_years_first_five = math.ceil(end_age - (end_age * 0.05))
        contribution_years_next_twenty = math.ceil(end_age - (end_age * 0.2))

        for i in range(start_age, end_age, 1):
            yearly_return = 0.08 if i < years_to_flip_interest else 0.06
            contribution = 0

            # Calculate the contribution
            # first 5% is small contribution
            # next 20% is heavy, then 0 until you have to take money out
            if i < contribution_years_first_five:
                contribution = 15000
            elif i < contribution_years_next_twenty:
                contribution = 40000
            elif i < years_to_flip_interest:
                contribution = 0 
            else:
                contribution = 0

            coast_savings_to_add = CoastFireSavings(
                age=i,
                year=year,
                contribution=contribution,
                yearlyReturn=yearly_return
            )
            coast_savings.append(coast_savings_to_add)
            year += 1

    # Now that the list of CoastFireSavings is populated with the required fields,
    # it's time to populate the rest of the calculations for a potential Coast FIRE
    for i in range(0, len(coast_savings)):
        if i == 0:
            coast_savings[i].total = (current_balance + coast_savings[i].contribution) * (coast_savings[i].yearlyReturn + 1)
        else:
            coast_savings[i].total = (coast_savings[i-1].total + coast_savings[i].contribution) * (coast_savings[i].yearlyReturn + 1)

    return coast_savings
