import math
import pandas as pd
import numpy as np

from logzero import logger


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


def loan_payments_calc(loan_amount, number_of_years, rate_of_interest, frequency="monthly"):
    frequency_int = convert_frequency(frequency, as_int=True)
    return np.pmt(rate = (to_percentage(rate_of_interest) / frequency_int), nper = number_of_years * frequency_int, pv = -loan_amount)


def loan_payments_calc_as_table(loan_amount, number_of_years, rate_of_interest, frequency="monthly"):
    payments = loan_payments_calc(loan_amount, number_of_years, rate_of_interest, frequency)
    interest = to_percentage(rate_of_interest)
    frequency_int = convert_frequency(frequency, as_int=True)
    frequency_num = frequency_int * number_of_years
    frequency_text = _frequency_text[frequency]

    loan_df = np.zeros((frequency_num, 6))
    loan_df = pd.DataFrame(loan_df)
    loan_df.columns = [frequency_text, "initialBalance", "payment", "interest",
                                "principal", "endingBalance"]
    loan_df.iloc[0, 0] = 1
    loan_df.iloc[0, 1] = loan_amount
    loan_df.iloc[0, 2] = payments
    loan_df.iloc[0, 3] = loan_amount * (interest / frequency_int)
    loan_df.iloc[0, 4] = payments - (loan_amount * (interest / frequency_int))
    loan_df.iloc[0, 5] = loan_amount - (payments - (loan_amount * (interest / frequency_int)))
    for i in range(1, frequency_num):
        loan_df.iloc[i, 0] = i + 1
        loan_df.iloc[i, 1] = loan_df.iloc[(i - 1), 5]
        loan_df.iloc[i, 2] = payments
        loan_df.iloc[i, 3] = loan_df.iloc[i, 1] * (interest / frequency_int)
        loan_df.iloc[i, 4] = payments - (loan_df.iloc[i, 1] * (interest / frequency_int))
        loan_df.iloc[i, 5] = loan_df.iloc[i, 1] - (payments - (loan_df.iloc[i, 1] * (interest / frequency_int)))
    
    loan_df = loan_df.round(2)
    loan_df[frequency_text] = loan_df[frequency_text].astype(int)

    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        return loan_df


# gets detailed statistics from a payments_df
# TODO: consider deleting, not really needed
def loan_payments_calc_stats(loan_amount, number_of_years, rate_of_interest, frequency="monthly"):
    payments_df = loan_payments_calc_as_table(loan_amount, number_of_years, rate_of_interest, frequency)

    # if you were to half the years
    half_number_of_years = math.ceil(number_of_years / 2)
    payments_half_df = loan_payments_calc_as_table(loan_amount, half_number_of_years, rate_of_interest, frequency)

    # if you were to reduce the years by 1
    reduced_by_1_number_of_years = number_of_years - 1
    payments_reduced_by_1_df = loan_payments_calc_as_table(loan_amount, reduced_by_1_number_of_years, rate_of_interest, frequency)

    # if you were to reduce the years by 30%
    reduced_by_30perc_number_of_years = math.ceil(number_of_years * 0.7)
    payments_reduced_by_30perc_df = loan_payments_calc_as_table(loan_amount, reduced_by_30perc_number_of_years, rate_of_interest, frequency)

    # if you were to reduce your rate of interest by 25%
    reduced_by_25perc_rate_of_interest = rate_of_interest * 0.75
    payments_roi_reduced_by_25perc_df = loan_payments_calc_as_table(loan_amount, number_of_years, reduced_by_25perc_rate_of_interest, frequency)

    # if you were to reduce your loan amount by 25%
    reduced_by_25perc_loan_amount = loan_amount * 0.75
    payments_reduced_by_25perc_loan_amount_df = loan_payments_calc_as_table(reduced_by_25perc_loan_amount, number_of_years, rate_of_interest, frequency)

    data = {
        "loan": [loan_amount, loan_amount, loan_amount, loan_amount, loan_amount, reduced_by_25perc_loan_amount],
        "interest": [rate_of_interest, rate_of_interest, rate_of_interest, rate_of_interest, reduced_by_25perc_rate_of_interest, rate_of_interest],
        "years": [
            number_of_years,
            reduced_by_1_number_of_years,
            half_number_of_years,
            reduced_by_30perc_number_of_years,
            number_of_years,
            number_of_years
        ],
        "frequency": [frequency, frequency, frequency, frequency, frequency, frequency],
        "totalInterest": [
            payments_df["interest"].sum(),
            payments_reduced_by_1_df["interest"].sum(),
            payments_half_df["interest"].sum(),
            payments_reduced_by_30perc_df["interest"].sum(),
            payments_roi_reduced_by_25perc_df["interest"].sum(),
            payments_reduced_by_25perc_loan_amount_df["interest"].sum()
        ],
        "totalPayments": [
            payments_df["payment"].sum(),
            payments_reduced_by_1_df["payment"].sum(),
            payments_half_df["payment"].sum(),
            payments_reduced_by_30perc_df["payment"].sum(),
            payments_roi_reduced_by_25perc_df["payment"].sum(),
            payments_reduced_by_25perc_loan_amount_df["payment"].sum()
        ],
        "description": [
            "original loan payments",
            "number of years reduced by 1",
            "number of years reduced by half",
            "number of years reduced by 30%",
            "rate of interest reduced by 25%",
            "loan amount reduced by 25%"
        ]
    }

    data_df = pd.DataFrame(data, columns=["loan", "interest", "years", "frequency", "totalInterest", "totalPayments", "description"])
    return data_df


# calculates new loan payments based on the new_ input
def loan_payments_calc_custom_stats(loan_amount, number_of_years, rate_of_interest, frequency="monthly",
    new_loan_amount=None,
    new_number_of_years=None,
    new_rate_of_interest=None,
    new_frequency=None):
    payments_df = loan_payments_calc_as_table(loan_amount, number_of_years, rate_of_interest, frequency)

    updated_loan_amount = new_loan_amount if new_loan_amount != None else loan_amount
    updated_number_of_years= new_number_of_years if new_number_of_years != None else number_of_years
    updated_rate_of_interest = new_rate_of_interest if new_rate_of_interest != None else rate_of_interest
    updated_frequency = new_frequency if new_frequency != None else frequency

    updated_payments_df = loan_payments_calc_as_table(updated_loan_amount, 
        updated_number_of_years, 
        updated_rate_of_interest, 
        updated_frequency)

    data = {
        "loan": [loan_amount, updated_loan_amount],
        "interest": [rate_of_interest, updated_rate_of_interest],
        "years": [number_of_years, updated_number_of_years],
        "frequency": [frequency, updated_frequency],
        "totalInterest": [payments_df["interest"].sum(), updated_payments_df["interest"].sum()],
        "totalPayments": [payments_df["payment"].sum(), updated_payments_df["payment"].sum()],
        "description": ["original loan payments", "updated loan payments"]
    }

    data_df = pd.DataFrame(data, columns=["loan", "interest", "years", "frequency", "totalInterest", "totalPayments", "description"])
    return data_df


# same as loan_payments_calc_custom_stats() but accepts only multiple new_* params
def loan_payments_calc_custom_multiple_stats(loan_amount, number_of_years, rate_of_interest, frequency="monthly",
    new_loan_amounts=None,
    new_number_of_years=None,
    new_rate_of_interests=None,
    new_frequencies=None):
    if type(new_loan_amounts) is not list or type(new_number_of_years) is not list or type(new_rate_of_interests) is not list or type(new_frequencies) is not list:
        raise ValueError("new_* params must all be lists")
    
    it = iter([new_loan_amounts, new_number_of_years, new_rate_of_interests, new_frequencies])
    the_len = len(next(it))
    if not all(len(l) == the_len for l in it):
        raise ValueError("not all new_* lists have same length")

    payments_df = loan_payments_calc_as_table(loan_amount, number_of_years, rate_of_interest, frequency)

    data = {
        "loan": [loan_amount],
        "interest": [rate_of_interest],
        "years": [number_of_years],
        "frequency": [frequency],
        "totalInterest": [payments_df["interest"].sum()],
        "totalPayments": [payments_df["payment"].sum()],
        "description": ["original loan payments"]
    }

    for i in range(0, len(new_loan_amounts)):
        updated_payments_df = loan_payments_calc_as_table(new_loan_amounts[i], 
            new_number_of_years[i], 
            new_rate_of_interests[i], 
            new_frequencies[i])

        data["loan"].append(new_loan_amounts[i])
        data["interest"].append(new_rate_of_interests[i])
        data["years"].append(new_number_of_years[i])
        data["frequency"].append(new_frequencies[i])
        data["totalInterest"].append(updated_payments_df["interest"].sum())
        data["totalPayments"].append(updated_payments_df["payment"].sum())
        data["description"].append("updated loan payments")

    data_df = pd.DataFrame(data, columns=["loan", "interest", "years", "frequency", "totalInterest", "totalPayments", "description"])
    return data_df


def simple_interest_calc(principal_amount, rate_of_interest, number_of_years):
    return (principal_amount * to_percentage(rate_of_interest) * number_of_years) / 100


def equated_monthly_installment_calc(principal_amount, rate_of_interest, number_of_months):
    interest = to_percentage(rate_of_interest)
    return (principal_amount * interest * (pow(1 + interest, number_of_months))) / ((pow(1 + interest, number_of_months)) - 1)


def doubling_time_with_continuous_compounding(rate_of_interest, frequency="yearly"):
    interest = to_percentage(rate_of_interest)
    return (np.log(2) / interest)


"""
source: https://financeformulas.net/Future_Value_of_Annuity.html

The future value of an annuity formula is used to calculate what the value at a future date would be for a series of periodic payments.

The future value of an annuity formula assumes that

1. The rate does not change
2. The first payment is one period away
3. The periodic payment does not change
"""
def future_value_calc(periodic_payment, rate_of_interest, number_of_years, frequency="yearly"):
    interest = to_percentage(rate_of_interest)
    frequency_int = number_of_years * convert_frequency(frequency, as_int=True)
    return periodic_payment * ((pow(1 + interest, frequency_int) - 1) / interest)