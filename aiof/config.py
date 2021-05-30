import os

from pydantic import BaseSettings
from typing import Optional, List
from functools import lru_cache

from aiof.data.analytics import Analytics


class Settings(BaseSettings):
    DefaultRoundingDigit: int = os.getenv("DefaultRoundingDigit", 2)
    DefaultFrequency: int = os.getenv("DefaultFrequency", 12)
    DefaultInterest: float = os.getenv("DefaultInterest", 7)
    DefaultHysInterest: float = os.getenv("DefaultHysInterest", 1.75)
    DefaultAverageBankInterest: float = os.getenv("DefaultAverageBankInterest", 0.06)
    DefaultInvestmentFee: float = os.getenv("DefaultFee", 0.50)
    DefaultTaxDrag: float = os.getenv("DefaultTaxDrag", 0.50)
    DefaultChild: int = os.getenv("DefaultChild", 2)

    DefaultYears: List[int] = [ 2, 5, 10, 20, 30 ]
    DefaultShortYears: List[int] = [ 5, 10, 30 ]
    DefaultInterests: list = [ 
        2,
        4,
        6,
        8
    ]
    DefaultFrequencies: list = [
        365,
        12,
        1        
    ]
    DefaultFees: list = [
        0.10,
        0.50,
        1.00,
        1.50,
        2.00,
        2.50,
        3.00,
    ]
    DefaultChildren: list = [
        1,
        2,
        3,
        4
    ]
    
    Frequencies: dict = {
        "daily": 365,
        "monthly": 12,
        "quarterly": 4,
        "half-year": 2,
        "yearly": 1
    }
    FrequenciesMap: dict = {
        "daily": "day",
        "monthly": "month",
        "quarterly": "quarter",
        "half-year": "half-year",
        "yearly": "year"
    }

    # FI specific
    DefaultTenMillion: list = [
        1000000,
        2000000,
        3000000,
        4000000,
        5000000,
        6000000,
        7000000,
        8000000,
        9000000,
        10000000,
        100000000,
    ]
    DefaultTenMillionInterests: list = [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10
    ]
    # End FI specific

    cors_origins: list = [
        "http://localhost:4100",
        "http://localhost:1337"
    ]
    cors_allowed_methods: list = [
        "*"
    ]
    cors_allowed_headers: list = [
        "*"
    ]


    # Asset
    class AssetType(object):
        CASH        = "cash"
        CAR         = "car"
        HOUSE       = "house"
        INVESTMENT  = "investment"
        STOCK       = "stock"
        FOUROHONEK  = "401(k)"
        OTHER       = "other"

    AssetTypes = [
        AssetType.CASH,
        AssetType.CAR,
        AssetType.HOUSE,
        AssetType.INVESTMENT,
        AssetType.STOCK,
        AssetType.FOUROHONEK,
        AssetType.OTHER
    ]

    # Liability
    LiabilityTypes = [
        "personal loan",
        "student loan",
        "auto loan",
        "auto lease",
        "credit card",
        "rent",
        "mortgage",
        "house renovation",
        "rv",
        "other"
    ]

    # Goal
    class GoalType(object):
        GENERIC         = "generic"
        TRIP            = "trip"
        BUYAHOME        = "buyAHome"
        BUYACAR         = "buyACar"
        SAVEFORCOLLEGE  = "saveForCollege"

    GoalTypes = [
        GoalType.GENERIC,
        GoalType.TRIP,
        GoalType.BUYAHOME,
        GoalType.BUYACAR,
        GoalType.SAVEFORCOLLEGE,
    ]


    # Analytics
    AnalyticsDebtToIncomeAcceptableLiabilityTypes = [
        "personal loan",
        "student loan",
        "auto loan",
        "credit card",
        "rent",
        "mortgage",
        "auto lease",
        "other"
    ]

    # Life event
    class LifeEventType(object):
        HAVING_A_CHILD = "having a child"
        BUYING_A_HOUSE = "buying a house"
        BUYING_A_CAR = "buying a car"
        SELLING_A_CAR = "selling a car"

    LifeEventTypes = [
        LifeEventType.HAVING_A_CHILD,
        LifeEventType.BUYING_A_HOUSE,
        LifeEventType.BUYING_A_CAR,
        LifeEventType.SELLING_A_CAR
    ]


@lru_cache()
def get_settings():
    return Settings()
