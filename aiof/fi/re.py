import math
import datetime
import numpy_financial as npf

import aiof.config as config

from aiof.data.fi import CoastFireSavings

from typing import List

# Configs
_settings = config.get_settings()
_round_dig = _settings.DefaultRoundingDigit


def coast_fire_savings(
    initial_interest_rate: float = 0.02,
    start_age: int = 33,
    end_age: int = 72,
    current_balance: float = 100000,
    coast_savings: List[CoastFireSavings] = None) -> List[CoastFireSavings]:
    """
    Show how savings will be affected for Coast FIRE

    Parameters
    ----------
    `initial_interest_rate` : float.
        initial interest amount used. defaults to `0.02`\n
    `start_age` : int.
        start age. defaults to `33`\n
    `end_age` : int.
        end age. defaults to `72`\n
    `current_balance` : int.
        current starting balance. defaults to `100,000`\n
    `coast_savings` : List[CoastFireSavings] or None.
        completely customizable coast fire savings list. defaults to being generated at runtime

    Notes
    ----------
    Based on https://www.reddit.com/r/financialindependence/comments/ja3nks/i_built_a_coastfire_compatible_savings_sheet/
    """
    years = end_age - start_age
    percentage_to_flip_interest = 0.3
    years_to_flip = math.ceil(end_age - (years * percentage_to_flip_interest))

    # If coast_savings is None, then generate it
    if coast_savings is None:
        coast_savings = []
        year = datetime.datetime.now().year
        contribution_years_first_five = math.ceil(start_age + (years * 0.05))
        contribution_years_next_twenty = math.ceil(contribution_years_first_five + (years * 0.2))

        for i in range(start_age, end_age + 1, 1):
            yearly_return = 0.08 if i < years_to_flip else 0.06
            contribution = 0

            # Calculate the contribution
            # first 5% is small contribution
            # next 20% is heavy, then 0 until you have to take money out
            if i < contribution_years_first_five:
                contribution = 15000
            elif i < contribution_years_next_twenty:
                contribution = 40000
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
        # Update contributions after flip year to -, meaning they're being withdrawn
        if i + start_age >= years_to_flip:
            coast_savings[i].contribution = -coast_savings[i - 1].withdrawFour

        if i == 0:
            coast_savings[i].total = (current_balance + coast_savings[i].contribution) * (coast_savings[i].yearlyReturn + 1)
        else:
            coast_savings[i].total = (coast_savings[i-1].total + coast_savings[i].contribution) * (coast_savings[i].yearlyReturn + 1)
        coast_savings[i].initialEarning = coast_savings[i].total * coast_savings[i].yearlyReturn
        coast_savings[i].withdrawFour = coast_savings[i].total * 0.04
        coast_savings[i].withdrawThree = coast_savings[i].total * 0.03
        coast_savings[i].withdrawTwo = coast_savings[i].total * 0.02

        coast_savings[i].presentValueFour = -npf.pv(
            rate=initial_interest_rate,
            nper=1,
            pmt=0,
            fv=coast_savings[i].withdrawFour,
            when='end')
        coast_savings[i].presentValueThree = -npf.pv(
            rate=initial_interest_rate,
            nper=1,
            pmt=0,
            fv=coast_savings[i].withdrawThree,
            when='end')
        coast_savings[i].presentValueTwo = -npf.pv(
            rate=initial_interest_rate,
            nper=1,
            pmt=0,
            fv=coast_savings[i].withdrawTwo,
            when='end')

    return coast_savings
