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


def compound_interest_calc(principal_amount, number_of_years, rate_of_interest, frequency = "yearly"):
    frequency_float = convert_frequency(frequency)
    return principal_amount * (pow(1 + (rate_of_interest / frequency_float), frequency_float * number_of_years))