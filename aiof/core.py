import json
import pandas as pd

import aiof.helpers as helpers


def frequencies():
    return list(helpers._frequency.keys())


def loan_payments_calc_as_table(content_as_json, frequency="monthly"):
    loan_amount = content_as_json["loanAmount"]
    number_of_years = content_as_json["numberOfYears"]
    rate_of_interest = content_as_json["rateOfInterest"]
    
    if loan_amount < 0:
        raise Exception("incorrect input. loan amount must be bigger than 0.")
    elif number_of_years < 0 or number_of_years > 150:
        raise Exception("incorrect input. number of years must be bigger than 0 and lower than 150")
    elif rate_of_interest < 0 or rate_of_interest > 100:
        raise Exception("incorrect input. rate of interest must be bigger than 0 and less than 100")

    return json.loads((helpers.loan_payments_calc_as_table(loan_amount, number_of_years, rate_of_interest, frequency)).to_json(orient="records"))


def test():
    print("Testing hello")