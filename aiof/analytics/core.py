import statistics as st
import pandas as pd
import numpy_financial as npf

import aiof.config as config
import aiof.helpers as helpers
import aiof.fi.core as fi

from aiof.data.analytics import Analytics, AssetsLiabilities
from aiof.data.asset import Asset, AssetFv
from aiof.data.liability import Liability
from aiof.data.life_event import LifeEventRequest, LifeEventResponse

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
    """
    Given a list of assets and liabilities, perform analytics on them

    Parameters
    ----------
    `assets` : List[Asset]\n
    `liabilities` : List[Liability]
    """
    assets_values = list(map(lambda x: x.value, assets))
    liabilities_values = list(map(lambda x: x.value, liabilities))

    assets_value_total = sum(assets_values)
    assets_value_mean = st.mean(assets_values)

    liabilities_value_total = sum(liabilities_values)
    liabilities_value_mean = st.mean(liabilities_values)

    diff = assets_value_total - liabilities_value_total

    analytics = Analytics()
    acceptable_assets = ["cash"]
    acceptable_liabilitites = ["credit card"]

    cash_assets = list(map(lambda x: x.value, filter(lambda x: x.typeName.lower() in acceptable_assets, assets)))
    total_cash_assets = sum(cash_assets)
    cc_liabilities = list(map(lambda x: x.value, filter(lambda x: x.typeName.lower() in acceptable_liabilitites, liabilities)))
    total_cc_liabilities = sum(cc_liabilities)

    # Calculate cashToCcRatio or ccToCashRatio
    if (total_cash_assets > 0 and total_cc_liabilities == 0):
        analytics.cashToCcRatio = round(100, _round_dig)
    elif (total_cc_liabilities > 0 and total_cash_assets == 0):
        analytics.ccToCashRatio = round(100, _round_dig)
    elif (total_cc_liabilities > 0 and total_cash_assets > 0 and total_cash_assets > total_cc_liabilities):
        analytics.cashToCcRatio = round((total_cc_liabilities / total_cash_assets) * 100, _round_dig)
    elif (total_cc_liabilities > 0 and total_cash_assets > 0 and total_cash_assets < total_cc_liabilities):
        analytics.ccToCashRatio = round((total_cash_assets / total_cash_assets) * 100, _round_dig)
    analytics.diff = round(diff, _round_dig)

    # If the asset is cash, then assume it's sitting in a bank account with an average interest
    analytics.assetsFv = assets_fv(assets=assets)

    # Debt to income ration calculation
    analytics.debtToIncomeRatio = debt_to_income_ratio_calc(income=150000, liabilities=liabilities)

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
    """
    Calculate assets' future value

    Parameters
    ----------
    `assets` : List[Asset]. 
        list of assets to calculate their future value
    """
    asset_fvs = []
    for year in _years:
        for asset in assets:
            interest = 0.0
            if (asset.typeName == "cash"):
                interest = _average_bank_interest
            elif (asset.typeName == "stock"):
                interest = _average_market_interest
            fv_asset = helpers.fv(interest=interest, years=year, pmt=0, pv=asset.value)
            asset_fvs.append(
                AssetFv(
                    year=year,
                    typeName=asset.typeName,
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
    Calculate debt to income ratio

    Parameters
    ----------
    `income` : float. 
        annual income\n
    `liabilities` : List[Liability].
        list of liabilities that will be used to calculate debt to income ratio\n
    """
    filtered_liabilities = [x for x in liabilities if x.typeName.lower() in _acceptable_liability_types and x.monthlyPayment is not None]

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
    Calculate debt to income ratio

    Parameters
    ----------
    `income` : float. 
        annual income\n
    `total_monthly_debt_payments` : float.
        total monthly debt payments. usually include credit cards, personal loan, student loan, etc.
    """
    return round(((total_monthly_debt_payments * 12) / income) * 100, _round_dig)


def life_event(req: LifeEventRequest) -> LifeEventResponse:
    """
    See how a life event impacts you

    Parameters
    ----------
    `req`: LifeEventRequest. 
        the life event request
    """
    # The idea is to have 2 or more sets of data frames. One will keep track of how your Assets will do over the years
    if req.type.lower() == "having a child":
        # How will Assets change over the years
        cost = fi.cost_of_raising_children(
            annual_expenses_start=10000,
            annual_expenses_increment=2000,
            children=[1],
            interests=[2],
            years=18)
        assets_df = helpers.assets_to_df(req.assets)
        total_cash = assets_df.loc[assets_df["typeName"] == "cash"]["value"].sum()
        total_stock = assets_df.loc[assets_df["typeName"] == "stock"]["value"].sum()

        # How it will effect your cash assets
        # What will happen to your assets if you have a child?
        cost_of_child = cost[0]
        monthly_cost = cost_of_child["cost"][0]["value"] / (cost_of_child["years"] * 12)
        years = list(range(1, cost_of_child["years"] + 1))

        life_event_cash_df = pd.DataFrame(index=years, columns=["year", "cash", "stock"])
        life_event_cash_df["year"] = years

        life_event_cash_df.iloc[0, 1] = -npf.fv(
            rate=(_settings.DefaultAverageBankInterest / 100) / 12,
            nper=12,
            pmt=-monthly_cost,
            pv=total_cash,
            when="end")

        life_event_cash_df.iloc[0, 2] = -npf.fv(
            rate=(_settings.DefaultInterest / 100) / 12,
            nper=12,
            pmt=0,
            pv=total_stock,
            when="end")

        for i in range(1, years[-1]):
            # Calculate the future value of your asset each time 
            # and then take out the expense
            life_event_cash_df.iloc[i, 1] = -npf.fv(
                rate=(_settings.DefaultAverageBankInterest / 100) / 12,
                nper=12,
                pmt=-monthly_cost,
                pv=life_event_cash_df.iloc[i - 1, 1],
                when="end")

            life_event_cash_df.iloc[i, 2] = -npf.fv(
                rate=(_settings.DefaultInterest / 100) / 12,
                nper=12,
                pmt=0,
                pv=life_event_cash_df.iloc[i - 1, 2],
                when="end")
        life_event_cash_df = life_event_cash_df.round(_round_dig)
        print(life_event_cash_df)

    elif req.type == "buying a house":
        print("test")
    elif req.type =="selling a car":
        print("selling a car")

    data = LifeEventResponse(
        currentAssets = req.assets,
        currentLiabilities = req.liabilities)

    return data