import aiof.helpers as helpers

def loan_calc(request_json):
    return loan_calc_internal(request_json["principalAmount"], request_json["numberOfMonths"], request_json["rateOfInterest"])

def loan_calc_internal(principal_amount, number_of_months, rate_of_interest):
    return helpers.loan_payments_calc(principal_amount, number_of_months / 12, rate_of_interest, frequency="monthly")