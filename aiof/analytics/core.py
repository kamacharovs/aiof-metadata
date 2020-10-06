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
    
    return AssetsLiabilities(
        assets=assets_values,
        liabilities=liabilities_values,
        assetsTotal=assets_value_total,
        assetsMean=assets_value_mean,
        liabilitiesTotal=liabilities_value_total,
        liabilitiesMean=liabilities_value_mean,
    )