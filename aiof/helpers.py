import math
import io
import pandas as pd
import numpy as np
import numpy_financial as npf

from logzero import logger
from decimal import Decimal

from aiof.config import Settings
from aiof.data.asset import ComparableAsset

# Configs
_settings = Settings()
_round_dig = _settings.DefaultRoundingDigit
_frequency = _settings.Frequencies
_frequency_text = _settings.FrequenciesMap


def convert_frequency(frequency, as_float=False, as_int=False):
    if frequency not in _frequency:
        raise Exception("frequency must be one of the following: " + ", ".join(_frequency))
    if as_float:
        return float(_frequency[frequency])
    elif as_int:
        return int(_frequency[frequency])
    return Decimal(_frequency[frequency])


def to_percentage(number):
    if number < 0 or number > 100:
        raise Exception("number can't be less than 0 or bigger than 100")
    return float(number) / 100


def compound_interest_calc(principal_amount, number_of_years, rate_of_interest, frequency="yearly"):
    frequency_float = convert_frequency(frequency, as_float=True)
    return principal_amount * (pow(1 + ((rate_of_interest / 100) / frequency_float), frequency_float * number_of_years))

def compound_interest_with_contributions_calc(
    principal_amount,
    number_of_years,
    rate_of_interest,
    contribution,
    frequency="monthly"):
    comp = compound_interest_calc(principal_amount, number_of_years, rate_of_interest, frequency)
    frequency_int = convert_frequency(frequency, as_int=True)
    r = rate_of_interest / 100
    raisedtopower2 = frequency_int * number_of_years
    ratedividedbynumberoftimes = r / frequency_int

    halfdone = ((((1 + (r / frequency_int)) ** raisedtopower2) -1) / ratedividedbynumberoftimes)
    futurevaluewithdeposits = contribution * halfdone

    return comp + futurevaluewithdeposits


def loan_payments_calc(
    loan_amount, 
    number_of_years, 
    rate_of_interest, 
    frequency="monthly"):
    frequency_int = convert_frequency(frequency, as_int=True)
    return npf.pmt(rate = (to_percentage(rate_of_interest) / frequency_int), nper = number_of_years * frequency_int, pv = -loan_amount)


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


# calculates new loan payments based on the new_ input
def loan_payments_calc_custom_stats(loan_amount, number_of_years, rate_of_interest, frequency="monthly",
    new_loan_amount=None,
    new_number_of_years=None,
    new_rate_of_interest=None,
    new_frequency=None):
    payments_df = loan_payments_calc_as_table(loan_amount, number_of_years, rate_of_interest, frequency)

    updated_loan_amount = new_loan_amount if new_loan_amount != None else loan_amount
    updated_number_of_years= new_number_of_years if new_number_of_years != None else number_of_years
    updated_rate_of_interest = new_rate_of_interest if new_rate_of_interest != None else rate_of_interest
    updated_frequency = new_frequency if new_frequency != None else frequency

    updated_payments_df = loan_payments_calc_as_table(updated_loan_amount, 
        updated_number_of_years, 
        updated_rate_of_interest, 
        updated_frequency)

    data = {
        "loan": [loan_amount, updated_loan_amount],
        "interest": [rate_of_interest, updated_rate_of_interest],
        "years": [number_of_years, updated_number_of_years],
        "frequency": [frequency, updated_frequency],
        "totalInterest": [payments_df["interest"].sum(), updated_payments_df["interest"].sum()],
        "totalPayments": [payments_df["payment"].sum(), updated_payments_df["payment"].sum()],
        "description": ["original loan payments", "updated loan payments"]
    }

    data_df = pd.DataFrame(data, columns=["loan", "interest", "years", "frequency", "totalInterest", "totalPayments", "description"])
    return data_df


# same as loan_payments_calc_custom_stats() but accepts only multiple new_* params
def loan_payments_calc_custom_multiple_stats(loan_amount, number_of_years, rate_of_interest, frequency="monthly",
    new_loan_amounts=None,
    new_number_of_years=None,
    new_rate_of_interests=None,
    new_frequencies=None):
    if type(new_loan_amounts) is not list or type(new_number_of_years) is not list or type(new_rate_of_interests) is not list or type(new_frequencies) is not list:
        raise ValueError("new_* params must all be lists")
    
    it = iter([new_loan_amounts, new_number_of_years, new_rate_of_interests, new_frequencies])
    the_len = len(next(it))
    if not all(len(l) == the_len for l in it):
        raise ValueError("not all new_* lists have same length")

    payments_df = loan_payments_calc_as_table(loan_amount, number_of_years, rate_of_interest, frequency)

    data = {
        "loan": [loan_amount],
        "interest": [rate_of_interest],
        "years": [number_of_years],
        "frequency": [frequency],
        "totalInterest": [payments_df["interest"].sum()],
        "totalPayments": [payments_df["payment"].sum()],
        "description": ["original loan payments"]
    }

    for i in range(0, len(new_loan_amounts)):
        updated_payments_df = loan_payments_calc_as_table(new_loan_amounts[i], 
            new_number_of_years[i], 
            new_rate_of_interests[i], 
            new_frequencies[i])

        data["loan"].append(new_loan_amounts[i])
        data["interest"].append(new_rate_of_interests[i])
        data["years"].append(new_number_of_years[i])
        data["frequency"].append(new_frequencies[i])
        data["totalInterest"].append(updated_payments_df["interest"].sum())
        data["totalPayments"].append(updated_payments_df["payment"].sum())
        data["description"].append("updated loan payments")

    data_df = pd.DataFrame(data, columns=["loan", "interest", "years", "frequency", "totalInterest", "totalPayments", "description"])
    return data_df


def simple_interest_calc(principal_amount, rate_of_interest, number_of_years):
    return (principal_amount * to_percentage(rate_of_interest) * number_of_years) / 100


def equated_monthly_installment_calc(principal_amount, rate_of_interest, number_of_months):
    interest = to_percentage(rate_of_interest)
    return (principal_amount * interest * (pow(1 + interest, number_of_months))) / ((pow(1 + interest, number_of_months)) - 1)


def doubling_time_with_continuous_compounding(rate_of_interest, frequency="yearly"):
    interest = to_percentage(rate_of_interest)
    return (np.log(2) / interest)


# Asset breakdown
# - Takes in a ComparableAsset and generates future values (fv) for different scenarios
# - For more information on each one, look at aiof.data.asset.Comparable class
# Returns: aiof.data.asset.ComparableAsset with all fields populated
def asset_breakdown(asset: ComparableAsset):
    asset.init_values()
    rate = ((asset.interest - asset.investmentFees - asset.taxDrag) / 100) / asset.frequency
    hys_rate = (asset.hysInterest / 100) / asset.frequency
    nper = asset.years * asset.frequency

    fv_end = -npf.fv(rate, nper, 0, asset.value, when='end')
    fv_begin = -npf.fv(rate, nper, 0, asset.value, when='begin')
    fv_with_contribution_end = -npf.fv(rate, nper, asset.contribution, asset.value, when='end')
    fv_with_contribution_begin = -npf.fv(rate, nper, asset.contribution, asset.value, when='begin')
    hys_fv_end = -npf.fv(hys_rate, nper, 0, asset.value, when='end')
    hys_fv_begin = -npf.fv(hys_rate, nper, 0, asset.value, when='begin')
    hys_fv_with_contribution_end = -npf.fv(hys_rate, nper, asset.contribution, asset.value, when='end')
    hys_fv_with_contribution_begin = -npf.fv(hys_rate, nper, asset.contribution, asset.value, when='begin')

    asset.marketValue = round(fv_end, _round_dig)
    asset.marketBeginValue = round(fv_begin, _round_dig)
    asset.marketValueBreakdown = asset_fv_breakdown_as_table(
        asset_value=asset.value,
        contribution=0,
        years=asset.years,
        rate=rate,
        frequency=asset.frequency).to_dict('records')

    asset.marketWithContributionValue = round(fv_with_contribution_end, _round_dig)
    asset.marketBeginWithContributionValue = round(fv_with_contribution_begin, _round_dig)
    asset.marketWithContributionValueBreakdown = asset_fv_breakdown_as_table(
        asset_value=asset.value,
        contribution=asset.contribution,
        years=asset.years,
        rate=rate,
        frequency=asset.frequency).to_dict('records')

    asset.hysValue = round(hys_fv_end, _round_dig)
    asset.hysBeginValue = round(hys_fv_begin, _round_dig)
    asset.hysValueBreakdown = asset_fv_breakdown_as_table(
        asset_value=asset.value,
        contribution=0,
        years=asset.years,
        rate=hys_rate,
        frequency=asset.frequency).to_dict('records')

    asset.hysWithContributionValue = round(hys_fv_with_contribution_end, _round_dig)
    asset.hysBeginWithContributionValue = round(hys_fv_with_contribution_begin, _round_dig)
    asset.hysWithContributionValueBreakdown = asset_fv_breakdown_as_table(
        asset_value=asset.value,
        contribution=asset.contribution,
        years=asset.years,
        rate=hys_rate,
        frequency=asset.frequency).to_dict('records')

    return asset


# Future value (fv) as a pandas.DataFrame table
# - Takes in the inputs and breaks down the future value (fv) for each year
def asset_fv_breakdown_as_table(
    asset_value,
    contribution,
    years,
    rate,
    frequency,
    when="end"):
    df = pd.DataFrame(np.zeros((years, 4)))
    df.columns = ["year", "contribution", "rate", "value"]
    asset_breakdown = -npf.fv(
        rate=rate, 
        nper=np.arange(frequency, ((years + 1) * frequency), frequency),
        pmt=contribution,
        pv=asset_value,
        when=when)
    for i in range(0, years):
        df.iloc[i, 0] = i + 1
        df.iloc[i, 1] = contribution
        df.iloc[i, 2] = rate
        df.iloc[i, 3] = asset_breakdown[i]
    df = df.round({"contribution": _round_dig, "rate": 4, "value": _round_dig})
    df["year"] = df["year"].astype(int)
    return df


# Export to .csv
# input: pandas DataFrame
# output: csv bytes
# can/will be used in FastAPI StreamResponse
def export_to_csv(df):
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    return iter([stream.getvalue()])