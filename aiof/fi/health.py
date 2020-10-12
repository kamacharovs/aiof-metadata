import aiof.config as config


# Configs
_settings = config.get_settings()
_round_dig = _settings.DefaultRoundingDigit


# Staying fit and healthy for a longer & better retirement

def bmi_imperial(
    weight: float,
    feet: float,
    inches: float):
    weight = weight if weight is not None else 165
    feet = feet if feet is not None else 6
    inches = inches if inches is not None else 0

    total_inches = feet * 12 + inches
    bmi = weight / (total_inches * total_inches) * 703
    return round(bmi, _round_dig)


def bmi_metric(
    weight: float,
    height: float):
    weight = weight if weight is not None else 75
    height = height if height is not None else 183

    bmi = weight / ((height * height) / 10000)
    return round(bmi, _round_dig)


if __name__ == "__main__":
    print(bmi_imperial(None, None, None))