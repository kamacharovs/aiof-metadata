from aiof.data.asset import Asset
from aiof.data.liability import Liability
"""
Given a list of Assets and Liabilities, how do they change when a major life event happens? Such as having a baby
"""

def analyze(
    assets: list,
    liabilities: list):
    for liability in liabilities:
        print(liability)