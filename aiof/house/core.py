import numpy as np

from aiof.helpers import to_percentage, convert_frequency


def mortgage_calc(principal_amount, rate_of_interest, number_of_periods, frequency="yearly"):
    interest = to_percentage(rate_of_interest)
    periods = convert_frequency(frequency) * number_of_periods
    numerator = interest * pow((1 + interest), periods)
    denominator = pow(1 + interest, periods) - 1
    return principal_amount * (numerator / denominator)