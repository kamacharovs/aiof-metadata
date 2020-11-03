import aiof.config as config


# Configs
_settings = config.get_settings()
_round_dig = _settings.DefaultRoundingDigit


def coast_fire_savings(
    initial_interest_rate: float = 2,
    start_year: int = 2020,
    start_age: int = 30,
    current_balance: float = 100000):
    end_age = 90