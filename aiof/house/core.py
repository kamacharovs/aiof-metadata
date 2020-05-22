import numpy as np

from aiof.helpers import to_percentage, convert_frequency


def mortgage_calc(principal_amount, rate_of_interest, number_of_periods, frequency="monthly"):
    interest = to_percentage(rate_of_interest)
    periods = convert_frequency(frequency)
    return principal_amount * ((pow(interest * (1 + interest), number_of_periods)) / (pow(1 + interest, number_of_periods) - 1))