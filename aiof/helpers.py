import pandas as pd
import numpy as np


_frequency = {
    "daily": 365,
    "monthly": 12,
    "quarterly": 4,
    "half-year": 2,
    "yearly": 1
}
_frequency_text = {
    "daily": "day",
    "monthly": "month",
    "quarterly": "quarter",
    "half-year": "half-year",
    "yearly": "year"
}


def convert_frequency(frequency, as_int=False):
    if frequency not in _frequency:
        raise Exception("frequency must be one of the following: " + ", ".join(_frequency))
    if as_int:
        return int(_frequency[frequency])
    return float(_frequency[frequency])


def to_percentage(number):
    if number < 0 or number > 100:
        raise Exception("number can't be less than 0 or bigger than 100")
    return float(number) / 100


def compound_interest_calc(principal_amount, number_of_years, rate_of_interest, frequency="yearly"):
    frequency_float = convert_frequency(frequency)
    return principal_amount * (pow(1 + ((rate_of_interest / 100) / frequency_float), frequency_float * number_of_years))


def loan_payments_calc(loan_amount, number_of_years, rate_of_interest, frequency="monthly"):
    frequency_int = convert_frequency(frequency, as_int=True)
    return np.pmt(rate = (to_percentage(rate_of_interest) / frequency_int), nper = number_of_years * frequency_int, pv = -loan_amount)


def loan_payments_calc_as_table(loan_amount, number_of_years, rate_of_interest, frequency="monthly"):
    payments = loan_payments_calc(loan_amount, number_of_years, rate_of_interest, frequency)
    interest = to_percentage(rate_of_interest)
    frequency_int = convert_frequency(frequency, as_int=True)
    frequency_num = frequency_int * number_of_years
    frequency_text = _frequency_text[frequency]

    loan_df = np.zeros((frequency_num, 6))
    loan_df = pd.DataFrame(loan_df)
    loan_df.columns = [frequency_text, "initialBalance", "payment", "interest",
                                "principal", "endingBalance"]
    loan_df.iloc[0, 0] = 1
    loan_df.iloc[0, 1] = loan_amount
    loan_df.iloc[0, 2] = payments
    loan_df.iloc[0, 3] = loan_amount * (interest / frequency_int)
    loan_df.iloc[0, 4] = payments - (loan_amount * (interest / frequency_int))
    loan_df.iloc[0, 5] = loan_amount - (payments - (loan_amount * (interest / frequency_int)))
    for i in range(1, frequency_num):
        loan_df.iloc[i, 0] = i + 1
        loan_df.iloc[i, 1] = loan_df.iloc[(i - 1), 5]
        loan_df.iloc[i, 2] = payments
        loan_df.iloc[i, 3] = loan_df.iloc[i, 1] * (interest / frequency_int)
        loan_df.iloc[i, 4] = payments - (loan_df.iloc[i, 1] * (interest / frequency_int))
        loan_df.iloc[i, 5] = loan_df.iloc[i, 1] - (payments - (loan_df.iloc[i, 1] * (interest / frequency_int)))
    
    loan_df = loan_df.round(2)
    loan_df[frequency_text] = loan_df[frequency_text].astype(int)

    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        return loan_df


def loan_payments_calc_as_table_stats(loan_amount, number_of_years, rate_of_interest, frequency="monthly"):
    payments_df = loan_payments_calc_as_table(loan_amount, number_of_years, rate_of_interest, frequency)
    payments_df_len = int(len(payments_df))
    payments_df_len_half = int(payments_df_len / 2)

    #if you were to invest in a high yield savings account
    hysa_amount = compound_interest_calc(loan_amount, number_of_years, 1.5)

    payments_stats = {
        "startingBalance": payments_df.iloc[0]["initialBalance"],
        "endingBalance": payments_df.iloc[payments_df_len - 1]["endingBalance"],
        "totalInterest": payments_df["interest"].sum(),
        "totalHalfInterest": payments_df.head(payments_df_len_half)["interest"].sum(),
        "totalPayments": payments_df["payment"].sum(),
        "totalHalfPayments": payments_df.head(payments_df_len_half)["payment"].sum(),
        "highYieldSavings": {
            "amount": hysa_amount
        }
    }
    
    print(payments_stats)


def simple_interest_calc(principal_amount, rate_of_interest, number_of_years):
    return (principal_amount * to_percentage(rate_of_interest) * number_of_years) / 100


def equated_monthly_installment_calc(principal_amount, rate_of_interest, number_of_months):
    interest = to_percentage(rate_of_interest)
    return (principal_amount * interest * (pow(1 + interest, number_of_months))) / ((pow(1 + interest, number_of_months)) - 1)


#create balance sheet list and total
def balance_sheet_calc(ending_balances):
    total_liabilities = 0
    for balance in ending_balances:
        total_liabilities += balance
    print(total_liabilities)


#balance_sheet_calc([20000,30000,40000,10000])
loan_payments_calc_as_table_stats(30000, 6, 4.5)