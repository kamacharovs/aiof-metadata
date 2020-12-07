import math
import numpy_financial as npf
import pandas as pd


def loan_calc(
    car_loan: float,
    interest: float,
    years: int):
    """
    Calculate car loan payments and details

    Parameters
    ----------
    `car_loan` : float or None.
        car loan amount. defaults to `35,000`\n
    `interest` : float or None.
        interest. defaults to `7`\n
    `years` : int or None.
        years for the loan. defaults to `5`
    """
    car_loan = car_loan if car_loan is not None else 35000
    interest = interest if interest is not None else 7
    years = years if years is not None else 5

    car_payments = npf.pmt(
        rate=interest / 100,
        nper= years,
        pv= -car_loan, 
        when='end')

    return car_payments
