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


def life_event_types() -> List[str]:
    """
    Get list of all life event types

    Returns
    ----------
    `List[str]`
    """
    return _settings.LifeEventTypes

def life_event_df_f(
    asset_type: str,
    years: int,
    start_amount: float,
    monthly_contribution: float,
    monthly_cost: float = None):
    """
    Create a life event `pandas.DataFrame` based on the asset type, total value and monthly contribution based on the number of years

    Parameters
    ----------
    `asset_type`: str. 
        the type of the asset. some examples are `cash`, `investment`, `stock`, etc.\n
    `years`: int.
        the number of years to create the `pandas.DataFrame` for\n
    `start_amount`: float.
        the start amount of the asset. this will be changing over the years based on default interests\n
    `monthly_contribution`: float.
        the monthly contribution to add on at the end of each year
    
    Returns
    ----------
    `pandas.DataFrame`
    """
    years_list = list(range(1, years + 1))
    interest = 0
    if asset_type in ["cash"]:
        interest = _settings.DefaultAverageBankInterest
    elif asset_type in ["stock", "investment"]:
        interest = _settings.DefaultInterest

    yearly_contribution = monthly_contribution * 12
    df = pd.DataFrame(index=years_list, columns=["year", f"{asset_type}", f"{asset_type}Contribution", f"{asset_type}WithContributions"])
    df["year"] = years_list
    df.iloc[0, 1] = -npf.fv(
        rate=(interest / 100) / 12,
        nper=12,
        pmt=-monthly_cost if monthly_cost is not None else 0,
        pv=start_amount,
        when="end")
    df.iloc[0, 2] = yearly_contribution
    df.iloc[0, 3] = -npf.fv(
        rate=(interest / 100) / 12,
        nper=12,
        pmt=monthly_contribution - monthly_cost if monthly_cost is not None else monthly_contribution,
        pv=start_amount,
        when="end")

    for i in range(1, years):
        df.iloc[i, 1] = -npf.fv(
            rate=(interest / 100) / 12,
            nper=12,
            pmt=-monthly_cost if monthly_cost is not None else 0,
            pv=df.iloc[i - 1, 1],
            when="end")
        df.iloc[i, 2] = yearly_contribution
        df.iloc[i, 3] = -npf.fv(
            rate=(interest / 100) / 12,
            nper=12,
            pmt=monthly_contribution - monthly_cost if monthly_cost is not None else monthly_contribution,
            pv=df.iloc[i - 1, 3],
            when="end")
    return df

def life_event(
    req: LifeEventRequest,
    as_json: bool = False) -> LifeEventResponse:
    """
    See how a life event impacts you

    Parameters
    ----------
    `req`: LifeEventRequest. 
        the life event request\n
    `as_json`: bool.
        whether to return the response as JSON. defaults to `False`

    Notes
    ----------
    There are a few assumption when it comes to your Assets. If they are of type `cash` then they are sitting in a bank with
    national average interest. If they are of type `stock` then they are invested in the market and the default market interest is used
    """
    data = LifeEventResponse(
        currentAssets = req.assets,
        currentLiabilities = req.liabilities)

    assets_df = helpers.assets_to_df(req.assets)

    if req.type.lower() == "having a child":
        # For each year you are raising a child, then your assets will change
        # For `cash` : take out cost of child, grow at bank interest rate
        # For `stock` : grow at default market rate
        # For `investment` : grow at default market rate
        child_year_to_be_raised_to = 18
        cost = fi.cost_of_raising_children(
            annual_expenses_start=10000,
            annual_expenses_increment=2000,
            children=[1],
            interests=[2],
            years=child_year_to_be_raised_to)
            
        total_cash = assets_df.loc[assets_df["typeName"] == "cash"]["value"].sum()
        total_stock = assets_df.loc[assets_df["typeName"] == "stock"]["value"].sum()
        total_investment = assets_df.loc[assets_df["typeName"] == "investment"]["value"].sum()

        cost_of_child = cost[0]
        monthly_cost = cost_of_child["cost"][0]["value"] / (cost_of_child["years"] * 12)
        years = list(range(1, cost_of_child["years"] + 1))

        life_event_df = pd.DataFrame(index=years, columns=["year"])
        life_event_df["year"] = years

        # Cash
        cash_df = life_event_df_f(
            asset_type              = "cash",
            years                   = child_year_to_be_raised_to,
            start_amount            = total_cash,
            monthly_contribution    = req.monthlyCashContribution if req.monthlyCashContribution is not None else 1000,
            monthly_cost            = monthly_cost)

        # Stock
        stock_df = life_event_df_f(
            asset_type              = "stock",
            years                   = child_year_to_be_raised_to,
            start_amount            = total_stock,
            monthly_contribution    = req.monthlyStockContribution if req.monthlyStockContribution is not None else 500)

        # Investment
        investment_df = life_event_df_f(
            asset_type              = "investment",
            years                   = child_year_to_be_raised_to,
            start_amount            = total_investment,
            monthly_contribution    = req.monthlyInvestmentContribution if req.monthlyInvestmentContribution is not None else 500)

        if not cash_df.isnull().values.any():
            life_event_df = pd.merge(life_event_df, cash_df, on="year", how="outer")
        if not investment_df.isnull().values.any():
            life_event_df = pd.merge(life_event_df, investment_df, on="year", how="outer")
        if not stock_df.isnull().values.any():
            life_event_df = pd.merge(life_event_df, stock_df, on="year", how="outer")

        life_event_df = life_event_df.round(_round_dig)
        data.event = life_event_df if not as_json else life_event_df.to_dict(orient="records")
    elif req.type.lower() == "buying a house":
        print("test")
    elif req.type.lower() == "selling a car":
        print("selling a car")

    return data