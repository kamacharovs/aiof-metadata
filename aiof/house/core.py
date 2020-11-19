import datetime
import json
import pandas as pd
import numpy_financial as npf

import aiof.config as config

from aiof.helpers import to_percentage, convert_frequency, loan_payments_calc_as_table, fv


# Configs
_settings = config.get_settings()
_round_dig = _settings.DefaultRoundingDigit


def house_mortgage_calc(principal_amount, rate_of_interest, number_of_periods, frequency="yearly"):
    interest = to_percentage(rate_of_interest)
    periods = convert_frequency(frequency) * number_of_periods
    numerator = interest * pow((1 + interest), float(periods))
    denominator = pow(1 + interest, float(periods)) - 1
    return principal_amount * (numerator / denominator)


def mortgage_calc(
    property_value: float = 300000,
    down_payment: float = 60000,
    interest_rate: float = 3.8,
    loan_term_years: int = 30,
    start_date: datetime = datetime.datetime.utcnow(),
    pmi: float = 0.5,
    home_insurance: float = 1000,
    monthly_hoa: float = 0,
    as_json: bool = False):
    """
    Calculate mortgage

    Parameters
    ----------
    `property_value` : float.
        value of the property. defaults to `300,000`\n
    `down_payment` : float.
        down payment for the property. defaults to `60,000`\n

    Notes
    ----------
    Based on https://www.mortgagecalculator.org/
    """
    # Fix interest rates to percentages
    interest_rate = interest_rate if interest_rate < 1 else interest_rate / 100
    pmi = pmi if pmi < 1 else pmi / 100

    payments_per_year = 12
    loan_amount = property_value - down_payment

    # Create the data frame
    rng = pd.date_range(start_date, periods=loan_term_years * payments_per_year, freq="MS")
    rng.name = "paymentDate"
    df = pd.DataFrame(index=rng, columns=["payment", "principalPaid", "interestPaid", "startingBalance", "endingBalance"], dtype="float")
    df.reset_index(inplace=True)
    df.index += 1
    df.index.name = "period"

    df["payment"] = -1 * npf.pmt(interest_rate / 12, loan_term_years * payments_per_year, loan_amount)
    df["principalPaid"] = -1 * npf.ppmt(interest_rate / payments_per_year, df.index, loan_term_years * payments_per_year, loan_amount)
    df["interestPaid"] = -1 * npf.ipmt(interest_rate / payments_per_year, df.index, loan_term_years * payments_per_year, loan_amount)
    
    # Populate the first ending balance, then the rest
    df["endingBalance"] = 0
    df.loc[1, "startingBalance"] = loan_amount
    df.loc[1, "endingBalance"] = loan_amount - df.loc[1, "principalPaid"]
    for period in range(2, len(df) + 1):
        prev_balance = df.loc[period - 1, "endingBalance"]
        principal_paid = df.loc[period, "principalPaid"]

        if prev_balance == 0:
            df.loc[period, ["payment", "principalPaid", "interestPaid","startingBalance", "endingBalance"]] == 0
            continue
        elif principal_paid <= prev_balance:
            df.loc[period, "startingBalance"] = prev_balance
            df.loc[period, "endingBalance"] = prev_balance - principal_paid
    
    df = df.round(_round_dig)

    return df.to_dict(orient="records") if as_json else df


def house_future_value_calc(periodic_payment, rate_of_interest, number_of_years, frequency="yearly"):
    return fv(
        interest=rate_of_interest, 
        years=number_of_years,
        pmt=periodic_payment,
        pv=0,
        frequency=frequency)


def house_sample():
    return loan_payments_calc_as_table(250000, 30, 3.25, "yearly")
