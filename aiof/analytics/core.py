import statistics as st
import numpy_financial as npf

import aiof.config as config
import aiof.helpers as helpers

from aiof.data.analytics import Analytics, AssetsLiabilities
from aiof.data.asset import Asset, AssetFv
from aiof.data.liability import Liability

from typing import List


"""
Given a list of Assets and Liabilities, how do they change when a major life event happens? Such as having a baby
"""
# Configs
_settings = config.get_settings()
_round_dig = _settings.DefaultRoundingDigit
_average_bank_interest = _settings.DefaultAverageBankInterest
_average_market_interest = _settings.DefaultInterest
_years = _settings.DefaultShortYears
_acceptable_liability_types = _settings.AnalyticsDebtToIncomeAcceptableLiabilityTypes


def analyze(
    assets: List[Asset],
    liabilities: List[Liability]) -> AssetsLiabilities:
    assets_values = list(map(lambda x: x.value, assets))
    liabilities_values = list(map(lambda x: x.value, liabilities))

    assets_value_total = sum(assets_values)
    assets_value_mean = st.mean(assets_values)

    liabilities_value_total = sum(liabilities_values)
    liabilities_value_mean = st.mean(liabilities_values)

    diff = assets_value_total - liabilities_value_total

    # Total cash in Assets
    analytics = Analytics()
    cash_assets = list(map(lambda x: x.value, filter(lambda x: x.type.lower() == "cash", assets)))
    total_cash_assets = sum(cash_assets)
    cc_liabilities = list(map(lambda x: x.value, filter(lambda x: x.type.lower() == "credit card", liabilities)))
    total_cc_liabilities = sum(cc_liabilities)

    if (total_cc_liabilities > 0 and total_cash_assets > 0 and total_cash_assets > total_cc_liabilities):
        analytics.cashToCcRation = round((total_cc_liabilities / total_cash_assets) * 100, _round_dig)
    elif (total_cc_liabilities > 0 and total_cash_assets > 0 and total_cash_assets < total_cc_liabilities):
        analytics.ccToCashRatio = round((total_cash_assets / total_cash_assets) * 100, _round_dig)
    analytics.diff = round(diff, _round_dig)

    # If the asset is cash, then assume it's sitting in a bank account with an average interest
    analytics.assetsFv = assets_fv(assets)

    return AssetsLiabilities(
        assets=assets_values,
        liabilities=liabilities_values,
        assetsTotal=round(assets_value_total, _round_dig),
        assetsMean=round(assets_value_mean, _round_dig),
        liabilitiesTotal=round(liabilities_value_total, _round_dig),
        liabilitiesMean=round(liabilities_value_mean, _round_dig),
        analytics=analytics
    )


def assets_fv(
    assets: List[Asset]) -> List[AssetFv]:
    asset_fvs = []
    for year in _years:
        for asset in assets:
            interest = 0.0
            if (asset.type == "cash"):
                interest = _average_bank_interest
            elif (asset.type == "stock"):
                interest = _average_market_interest
            fv_asset = helpers.fv(interest=interest, years=year, pmt=0, pv=asset.value)
            asset_fvs.append(
                AssetFv(
                    year=year,
                    type=asset.type,
                    interest=interest,
                    pv=asset.value,
                    fv=round(fv_asset, _round_dig)
                )
            )
    return asset_fvs
                

def debt_to_income_ratio_calc(
    income: float,
    liabilities: List[Liability]) -> float:
    """
    Calculate your debt to income ratio

    Parameters
    ----------
    `income` : float. 
        annual income\n
    `liabilities` : List[Liability].
        list of liabilities that will be used to calculate your debt to income ratio\n
    """
    filtered_liabilities = [x for x in liabilities if x.type.lower() in _acceptable_liability_types and x.monthlyPayment is not None]

    if len(filtered_liabilities) == 0:
        return 0.0
    
    total_liabilities_payments = 0.0
    for liability in filtered_liabilities:
        liability_monthly_payment = 0

        # Check if there are cases where .monthlyPayment is 0 and .years is there
        # then calculate the monthly payment
        if liability.years is not None and liability.years > 0 and liability.monthlyPayment == 0:
            liability_monthly_payment = (liability.value / liability.years) / 12
        else:
            liability_monthly_payment = liability.monthlyPayment
        total_liabilities_payments += liability_monthly_payment

    return debt_to_income_ratio_basic_calc(income, total_liabilities_payments)


def debt_to_income_ratio_basic_calc(
    income: float,
    total_monthly_debt_payments: float) -> float:
    """
    Calculate your debt to income ratio

    Parameters
    ----------
    `income` : float. 
        annual income\n
    `total_monthly_debt_payments` : float.
        total monthly debt payments. usually include credit cards, personal loan, student loan, etc.\n
    """
    return ((total_monthly_debt_payments * 12) / income) * 100
