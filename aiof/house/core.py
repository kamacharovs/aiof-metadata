import numpy as np
import pandas as pd

from aiof.helpers import to_percentage, convert_frequency, loan_payments_calc_as_table, future_value_calc


def house_mortgage_calc(principal_amount, rate_of_interest, number_of_periods, frequency="yearly"):
    interest = to_percentage(rate_of_interest)
    periods = convert_frequency(frequency) * number_of_periods
    numerator = interest * pow((1 + interest), float(periods))
    denominator = pow(1 + interest, float(periods)) - 1
    return principal_amount * (numerator / denominator)


def house_future_value_calc(periodic_payment, rate_of_interest, number_of_years, frequency="yearly"):
    return future_value_calc(periodic_payment, rate_of_interest, number_of_years, frequency)


def house_sample():
    return loan_payments_calc_as_table(250000, 30, 3.25, "yearly")