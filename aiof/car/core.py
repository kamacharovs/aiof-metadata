import math
import numpy as np
import numpy_financial as npf
import pandas as pd

import aiof.config as config


# Configs
_settings = config.get_settings()
_round_dig = _settings.DefaultRoundingDigit


def loan_calc(
    car_loan: float = None,
    interest: float = None,
    years: int = None,
    as_json: bool = False):
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
    `as_json` : bool or False.
        return result as JSON. defaults to `False`
    """
    car_loan = car_loan if car_loan is not None else 35000
    interest = interest if interest is not None else 7
    years = years if years is not None else 5

    interest = interest / 100

    car_payments = npf.pmt(
        rate=interest,
        nper=years,
        pv=-car_loan, 
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

    return loan_df if not as_json else loan_df.to_dict(orient="records")
