import aiof.helpers as helpers


def frequencies():
    return list(helpers._frequency.keys())


def loan_payments_calc_as_table(content_as_json, frequency="monthly"):
    loan_amount = content_as_json["loanAmount"]
    number_of_years = content_as_json["numberOfYears"]
    rate_of_interest = content_as_json["rateOfInterest"]
    #TODO: add input (parameter) checks
    return helpers.loan_payments_calc_as_table(loan_amount, number_of_years, rate_of_interest, frequency)


def test():
    print("Testing hello")