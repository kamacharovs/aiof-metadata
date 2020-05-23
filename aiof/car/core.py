import aiof.helpers as helpers


def loan_calc(principal_amount, rate_of_interest, number_of_months):
    return helpers.loan_payments_calc(principal_amount, number_of_months / 12, rate_of_interest, frequency="monthly")