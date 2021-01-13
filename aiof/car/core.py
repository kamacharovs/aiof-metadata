import math
import numpy as np
import numpy_financial as npf
import pandas as pd

import aiof.config as config

from aiof.data.car import CarLoanResponse

from random import randrange


# Configs
_settings = config.get_settings()
_round_dig = _settings.DefaultRoundingDigit


def loan_calc(
    car_loan: float = None,
    interest: float = None,
    years: int = None,
    data_as_json: bool = False) -> CarLoanResponse:
    """
    Calculate car loan payments and details

    Parameters
    ----------
    `car_loan` : float or None.
        car loan amount. defaults to `35,000`\n
    `interest` : float or None.
        interest. defaults to `7`\n
    `years` : int or None.
        years for the loan. defaults to `5`\n
    `data_as_json` : bool or False.
        return data (DataFrame) result as JSON. defaults to `False`
    """
    car_loan = car_loan if car_loan is not None else 35000
    interest = interest if interest is not None else 7
    years = years if years is not None else 5

    interest = interest / 100

    car_payments = npf.pmt(
        rate=interest,
        nper=years,
        pv=-car_loan, 
        fv=0,
        when='end')
    car_payments_monthly = npf.pmt(
        rate=interest / 12,
        nper=years * 12,
        pv=-car_loan, 
        fv=0,
        when='end')

    loan_df = np.zeros((years, 6))
    loan_df = pd.DataFrame(loan_df)
    loan_df.columns = ["year", "startingBalance", "payments", "interestPaid", "principalPaid", "endingBalance"]

    loan_df.iloc[0, 0] = 1
    loan_df.iloc[0, 1] = car_loan
    loan_df.iloc[0, 2] = car_payments
    loan_df.iloc[0, 3] = car_loan * interest
    loan_df.iloc[0, 4] = car_payments - (car_loan * interest)
    loan_df.iloc[0, 5] = car_loan - (car_payments - (car_loan * interest))
    for i in range(1, years):
        loan_df.iloc[i, 0] = i + 1
        loan_df.iloc[i, 1] = loan_df.iloc[(i - 1), 5]
        loan_df.iloc[i, 2] = car_payments
        loan_df.iloc[i, 3] = loan_df.iloc[i, 1] * interest
        loan_df.iloc[i, 4] = car_payments - (loan_df.iloc[i, 1] * interest)
        loan_df.iloc[i, 5] = loan_df.iloc[i, 1] - (car_payments - (loan_df.iloc[i, 1] * interest))
 
    loan_df = loan_df.round(_round_dig)

    resp = CarLoanResponse(
        carLoan = car_loan,
        interest = interest,
        years = years,
        monthlyPayment = round(car_payments_monthly, _round_dig),
        data = loan_df if not data_as_json else loan_df.to_dict(orient="records"))

    return resp


def value_depreciation_calc(
    loan_amount: float  = None,
    years: int          = None,
    as_json: bool       = False):
    """
    Calculates how much your car will depreciate over the years. 
    The assumptions are that your car's value decreases around 20% to 30% by the end of the first year. 
    From years two to six, depreciation ranges from 15% to 18% per year. 
    As a rule of thumb, in five years, cars lose 60% or more of their initial value
    """
    loan_amount = loan_amount if loan_amount is not None else 35000
    years = years if years is not None else 5

    first_year_avg_int = randrange(20, 30)
    two_to_six_years_avg_int = randrange(15, 18)
    remaining_years_int = 60 - (first_year_avg_int + two_to_six_years_avg_int)

    two_to_six_years_avg_int = (two_to_six_years_avg_int / 4) / 100 if years >= 6 else (two_to_six_years_avg_int / years - 1) / 100

    print("here")