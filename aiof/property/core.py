import datetime
import pandas as pd
import numpy_financial as npf
from pandas.core.frame import DataFrame

import aiof.config as config

from aiof.helpers import to_percentage, convert_frequency, loan_payments_calc_as_table, fv


# Configs
_settings = config.get_settings()
_round_dig = _settings.DefaultRoundingDigit


def mortgage_calc(
    property_value: float = None,
    down_payment: float = None,
    interest_rate: float = None,
    loan_term_years: int = None,
    start_date: datetime = None,
    pmi: float = None,
    property_insurance: float = None,
    monthly_hoa: float = None,
    include_yearly_breakdown: bool = False,
    as_json: bool = False):
    """
    Calculate mortgage

    Parameters
    ----------
    `property_value` : float.
        value of the property. defaults to `300,000`\n
    `down_payment` : float.
        down payment for the property. defaults to `60,000`\n
    `interest_rate` : float.
        annual interest rate. defaults to `3.8`\n
    `loan_term_years` : float.
        years in the loan term. defaults to `30`\n
    `start_date` : datetime.
        start date of the loan. defaults to `datetime.datetime.utcnow()`\n
    `pmi` : float.
        pmi interest rate. defaults to `0.5`\n
    `property_insurance` : float.
        annual property insurance. defaults to `1000`\n
    `monthly_hoa` : float.
        monthly hoa dues. defaults to `0`\n
    `as_json` : bool.
        whether to return the pandas.DataFrame as JSON. defaults to `False`\n

    Notes
    ----------
    Based on https://www.mortgagecalculator.org/
    """
    # Check for None
    property_value      = property_value if property_value is not None else 300000
    down_payment        = down_payment if down_payment is not None else 60000
    interest_rate       = interest_rate if interest_rate is not None else 3.8
    loan_term_years     = loan_term_years if loan_term_years is not None else 30
    start_date          = start_date if start_date is not None else datetime.datetime.utcnow()
    pmi                 = pmi if pmi is not None else 0.5
    property_insurance  = property_insurance if property_insurance is not None else 1000
    monthly_hoa         = monthly_hoa if monthly_hoa is not None else 0

    # Check and fix parameters
    interest_rate = interest_rate / 100
    pmi = pmi / 100
    payments_per_year = 12
    loan_amount = property_value - down_payment
    
    # Validation
    if loan_amount < 0:
        raise ValueError("Loan Amount (property value minus down payment) cannot be negative")
    elif down_payment < 0:
        raise ValueError("Down payment cannot be negative")
    elif loan_term_years < 0 or loan_term_years > 100:
        raise ValueError("Loan term years must be between 1 and 100")
    elif interest_rate > 1 or interest_rate < 0:
        raise ValueError("Interest rate cannot be negative or bigger than 100%")
    elif pmi > 1 or pmi < 0:
        raise ValueError("PMI rate cannot be negative or bigger than 100%")
    elif property_insurance < 0:
        raise ValueError("Property insurance cannot be negative")
    elif monthly_hoa < 0:
        raise ValueError("Monthly HOA cannot be negative")


    # Create and initially populate the data frame
    rng = pd.date_range(start_date, periods=loan_term_years * payments_per_year, freq="MS")
    rng.name = "paymentDate"
    df = pd.DataFrame(index=rng, columns=["payment", "principalPaid", "interestPaid", "startingBalance", "endingBalance"], dtype="float")
    df.reset_index(inplace=True)
    df.index += 1
    df.index.name = "period"

    df["payment"] = -npf.pmt(interest_rate / 12, loan_term_years * payments_per_year, loan_amount)
    df["principalPaid"] = -npf.ppmt(interest_rate / payments_per_year, df.index, loan_term_years * payments_per_year, loan_amount)
    df["interestPaid"] = -npf.ipmt(interest_rate / payments_per_year, df.index, loan_term_years * payments_per_year, loan_amount)
    
    # Populate the first ending balance, then the rest
    df["endingBalance"] = 0
    df.loc[1, "startingBalance"] = loan_amount
    df.loc[1, "endingBalance"] = loan_amount - df.loc[1, "principalPaid"]
    for period in range(2, len(df) + 1):
        prev_balance = df.loc[period - 1, "endingBalance"]
        principal_paid = df.loc[period, "principalPaid"]

        df.loc[period, "startingBalance"] = prev_balance
        if prev_balance == 0:
            df.loc[period, ["payment", "principalPaid", "interestPaid", "startingBalance", "endingBalance"]] == 0
            continue
        elif principal_paid <= prev_balance:
            df.loc[period, "endingBalance"] = prev_balance - principal_paid
    
    df = df.round(_round_dig)

    if include_yearly_breakdown:
        return {
            "data": df.to_dict(orient="records"),
            "breakdown": mortgage_calc_yearly_breakdown(df).to_dict(orient="records")
        }
    else:
        return df if not as_json else { "data": df.to_dict(orient="records") }


def mortgage_calc_yearly_breakdown(mortgage_df: DataFrame):
    df = mortgage_df.copy()
    df["year"] = df["paymentDate"].dt.year
    unique_years = df["year"].unique()
    year_dfs = [df[df["year"] == y] for y in unique_years]
    
    total_df = pd.DataFrame(index=unique_years.tolist(), columns=["year", "startingBalance", "endingBalance", "totalPayment", "totalPrincipalPaid", "totalInterestPaid"], dtype="float")
    for year_df in year_dfs:
        total_df.loc[year_df.iloc[0]["year"]]["year"] = year_df.iloc[0]["year"]
        total_df.loc[year_df.iloc[0]["year"]]["startingBalance"] = year_df.iloc[0]["startingBalance"]
        total_df.loc[year_df.iloc[0]["year"]]["endingBalance"] = year_df.iloc[len(year_df) - 1]["endingBalance"]
        total_df.loc[year_df.iloc[0]["year"]]["totalPayment"] = year_df["payment"].sum()
        total_df.loc[year_df.iloc[0]["year"]]["totalPrincipalPaid"] = year_df["principalPaid"].sum()
        total_df.loc[year_df.iloc[0]["year"]]["totalInterestPaid"] = year_df["interestPaid"].sum()
    total_df["year"] = total_df["year"].astype(int)
    total_df = total_df.round(_round_dig)

    return total_df


def house_mortgage_calc(principal_amount, rate_of_interest, number_of_periods, frequency="yearly"):
    interest = to_percentage(rate_of_interest)
    periods = convert_frequency(frequency) * number_of_periods
    numerator = interest * pow((1 + interest), float(periods))
    denominator = pow(1 + interest, float(periods)) - 1
    return principal_amount * (numerator / denominator)


def house_future_value_calc(periodic_payment, rate_of_interest, number_of_years, frequency="yearly"):
    return fv(
        interest=rate_of_interest, 
        years=number_of_years,
        pmt=periodic_payment,
        pv=0,
        frequency=frequency)


def house_sample():
    return loan_payments_calc_as_table(250000, 30, 3.25, "yearly")
