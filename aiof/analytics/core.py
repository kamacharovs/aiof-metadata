import statistics as st
import numpy_financial as npf

import aiof.config as config
import aiof.helpers as helpers

from aiof.data.analytics import Analytics, AssetsLiabilities
from aiof.data.asset import Asset
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
_years = _settings.DefaultYears


def analyze(
    assets: List[Asset],
    liabilities: List[Liability]):
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
    assets_fv(assets)
    
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
    assets: List[Asset]):
    to_return_obj = []
    for year in _years:
        fv_obj = []
        for asset in assets:
            fv_asset = 0.0
            if (asset.type == "cash"):
                fv_asset = helpers.fv(interest=_average_bank_interest, years=year, pmt=0, pv=asset.value)
            elif (asset.type == "stock"):
                fv_asset = helpers.fv(interest=_average_market_interest, years=year, pmt=0, pv=asset.value)
            fv_obj.append(
                {
                    "type": asset.type,
                    "pv": asset.value,
                    "fv": fv_asset
                })
        
        to_return_obj.append(
            {
                "year": year,
                "fvs": fv_obj
            })
    print(to_return_obj)
                