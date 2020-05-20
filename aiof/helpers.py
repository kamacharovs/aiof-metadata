_frequency = [
    "daily",
    "monthly",
    "quarterly",
    "half-year",
    "yearly"
]


def convert_frequency(frequency):
    if frequency not in _frequency:
        raise Exception("frequency must be one of the following: " + ",".join(_frequency))

    if frequency == "daily":
        frequency_float = 365
    elif frequency == "monthly":
        frequency_float = 12
    elif frequency == "half-year":
        frequency_float = 6
    elif frequency == "yearly":
        frequency_float = 1

    return float(frequency_float)


def compound_interest(principal_amount, number_of_years, rate_of_interest, frequency = "yearly"):
    frequency_float = convert_frequency(frequency)
    return principal_amount * (1 + (rate_of_interest / (100 * frequency_float)) ** (frequency_float * number_of_years))