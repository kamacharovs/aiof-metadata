import pandas as pd
import numpy as np
import numpy_financial as npf


_frequency = {
    "daily": 365,
    "monthly": 12,
    "quarterly": 4,
    "half-year": 2,
    "yearly": 1
}
_frequency_text = {
    "daily": "day",
    "monthly": "month",
    "quarterly": "quarter",
    "half-year": "half-year",
    "yearly": "year"
}


def convert_frequency(frequency, as_int=False):
    if frequency not in _frequency:
        raise Exception("frequency must be one of the following: " + ", ".join(_frequency))
    if as_int:
        return int(_frequency[frequency])
    return float(_frequency[frequency])


def to_percentage(number):
    if number < 0 or number > 100:
        raise Exception("number can't be less than 0 or bigger than 100")
    return float(number) / 100


def compound_interest_calc(principal_amount, number_of_years, rate_of_interest, frequency="yearly"):
    frequency_float = convert_frequency(frequency)
    return principal_amount * (pow(1 + ((rate_of_interest / 100) / frequency_float), frequency_float * number_of_years))


def loan_payments_calc(loan_amount, number_of_years, rate_of_interest, frequency="yearly"):
    car_payments = npf.pmt(rate = to_percentage(rate_of_interest), nper = number_of_years, pv = -loan_amount)
    return car_payments / convert_frequency(frequency)

def loan_payments_calc_as_table(loan_amount, number_of_years, rate_of_interest):
    frequency = "yearly"
    car_payments = loan_payments_calc(loan_amount, number_of_years, rate_of_interest, frequency)
    interest = to_percentage(rate_of_interest)
    frequency_num = convert_frequency(frequency, as_int=True) * number_of_years
    frequency_text = _frequency_text[frequency]

    loan_df = np.zeros((frequency_num, 6))
    loan_df = pd.DataFrame(loan_df)
    loan_df.columns = [frequency_text, "initialBalance", "payments", "interest",
                                "principal", "endingBalance"]
    loan_df.iloc[0, 0] = 1
    loan_df.iloc[0, 1] = loan_amount
    loan_df.iloc[0, 2] = car_payments
    loan_df.iloc[0, 3] = loan_amount * interest
    loan_df.iloc[0, 4] = car_payments - (loan_amount * interest)
    loan_df.iloc[0, 5] = loan_amount - (car_payments - (loan_amount * interest))
    for i in range(1, frequency_num):
        loan_df.iloc[i, 0] = i + 1
        loan_df.iloc[i, 1] = loan_df.iloc[(i - 1), 5]
        loan_df.iloc[i, 2] = car_payments
        loan_df.iloc[i, 3] = loan_df.iloc[i, 1] * interest
        loan_df.iloc[i, 4] = car_payments - (loan_df.iloc[i, 1] * interest)
        loan_df.iloc[i, 5] = loan_df.iloc[i, 1] - (car_payments - (loan_df.iloc[i, 1] * interest))
    
    loan_df = loan_df.round(2)
    loan_df[frequency_text] = loan_df[frequency_text].astype(int)

    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        return loan_df.to_json(orient="records")