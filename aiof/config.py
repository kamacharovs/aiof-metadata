from pydantic import BaseSettings


class Settings(BaseSettings):
    DefaultRoundingDigit: int = 2
    DefaultInterest: float = 7
    DefaultInterests: list = [ 
        2,
        4,
        6,
        8
    ]
    DefaultFrequency: int = 12
    DefaultFrequencies: list = [
        365,
        12,
        1        
    ]
    DefaultFee: float = 0.10
    DefaultFees: list = [
        0.10,
        0.50,
        1.00,
        1.50,
        2.00,
        2.50,
        3.00,
    ]
    DefaultChild: int = 2
    DefaultChildren: list = [
        1,
        2,
        3,
        4
    ]

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
        "http://localhost:4100"
    ]
    cors_allowed_methods: list = [
        "*"
    ]
    cors_allowed_headers: list = [
        "*"
    ]

