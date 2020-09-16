import aiof.helpers as helpers

def loan_calc(req):
    principal_amount = req["principalAmount"] if "principalAmount" in req else 150000
    number_of_months = req["numberOfMonths"] if "numberOfMonths" in req else 72
    rate_of_interest = req["rateOfInterest"] if "rateOfInterest" in req else 7
    return loan_calc_internal(
        principal_amount, 
        number_of_months,
        rate_of_interest)

def loan_calc_internal(
    principal_amount, 
    number_of_months,
    rate_of_interest):
    return helpers.loan_payments_calc(principal_amount, number_of_months / 12, rate_of_interest, frequency="monthly")