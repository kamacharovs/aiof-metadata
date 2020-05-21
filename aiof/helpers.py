import pandas as pd
import numpy_financial as npf


_frequency = {
    "daily": 365,
    "monthly": 12,
    "quarterly": 4,
    "half-year": 2,
    "yearly": 1
}


def convert_frequency(frequency):
    if frequency not in _frequency:
        raise Exception("frequency must be one of the following: " + ", ".join(_frequency))
    return float(_frequency[frequency])


def to_percentage(number):
    if number < 0 or number > 100:
        raise Exception("number can't be less than 0 or bigger than 100")
    return float(number) / 100


def compound_interest_calc(principal_amount, number_of_years, rate_of_interest, frequency = "yearly"):
    frequency_float = convert_frequency(frequency)
    return principal_amount * (pow(1 + ((rate_of_interest / 100) / frequency_float), frequency_float * number_of_years))


def loan_payments_calc(loan_amount, number_of_years, rate_of_interest, frequency = "yearly"):
    car_payments = npf.pmt(rate = to_percentage(rate_of_interest), nper = number_of_years, pv = -loan_amount)
    return car_payments / convert_frequency(frequency)