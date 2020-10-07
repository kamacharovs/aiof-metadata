import statistics as st

from aiof.data.analytics import AssetsLiabilities
from aiof.data.asset import Asset
from aiof.data.liability import Liability

"""
Given a list of Assets and Liabilities, how do they change when a major life event happens? Such as having a baby
"""

def analyze(
    assets: list,
    liabilities: list):
    assets_values = list(map(lambda x: x.value, assets))
    liabilities_values = list(map(lambda x: x.value, liabilities))

    assets_value_total = sum(assets_values)
    assets_value_mean = st.mean(assets_values)

    liabilities_value_total = sum(liabilities_values)
    liabilities_value_mean = st.mean(liabilities_values)

    dif = assets_value_total - liabilities_value_total

    # Total cash in Assets
    cash_to_cc_ratio = 0.0
    cc_to_cash_ratio = 0.0
    cash_assets = list(map(lambda x: x.value, filter(lambda x: x.type.lower() == "cash", assets)))
    total_cash_assets = sum(cash_assets)
    cc_liabilities = list(map(lambda x: x.value, filter(lambda x: x.type.lower() == "credit card", liabilities)))
    total_cc_liabilities = sum(cc_liabilities)
    if (total_cc_liabilities > 0 and total_cash_assets > 0 and total_cash_assets > total_cc_liabilities):
        cash_to_cc_ratio = (total_cc_liabilities / total_cash_assets) * 100
    elif (total_cc_liabilities > 0 and total_cash_assets > 0 and total_cash_assets < total_cc_liabilities):
        cc_to_cash_ratio = (total_cash_assets / total_cash_assets) * 100

    
    return AssetsLiabilities(
        assets=assets_values,
        liabilities=liabilities_values,
        assetsTotal=assets_value_total,
        assetsMean=assets_value_mean,
        liabilitiesTotal=liabilities_value_total,
        liabilitiesMean=liabilities_value_mean,
        analytics={
            "dif": dif,
            "cashToCcRatio": cash_to_cc_ratio,
            "ccToCashRatio": cc_to_cash_ratio
        }
    )
