from aiof.helpers import *


def loan_calc(principal_amount, rate_of_interest, number_of_months):
    return loan_payments_calc(principal_amount, number_of_months / 12, rate_of_interest, frequency="monthly")