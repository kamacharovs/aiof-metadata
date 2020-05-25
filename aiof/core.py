import aiof.helpers as helpers


def frequencies():
    return list(helpers._frequency.keys())


def loan_payments_calc_as_table(content, frequency="monthly"):
    loan_amount = content["loanAmount"]
    number_of_years = content["numberOfYears"]
    rate_of_interest = content["rateOfInterest"]
    #TODO: add input (parameter) checks
    return helpers.loan_payments_calc_as_table(loan_amount, number_of_years, rate_of_interest, frequency)