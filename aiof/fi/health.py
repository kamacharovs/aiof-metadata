import aiof.config as config


# Configs
_settings = config.get_settings()
_round_dig = _settings.DefaultRoundingDigit


# Staying fit and healthy for a longer & better retirement

def bmi_imperial(
    weight: float,
    feet: float,
    inches: float):
    """
    Calculate one's BMI (Body Mass Index) given one's weight (lbs), feet and inches

    Parameters
    ----------
    `weight` : float or None.
        one's weight in lbs. defaults to `165`\n
    `feet` : float or None.
        one's feet height. defaults to `6`\n
    `inches` : float or None.
        one's inches height. defaults to `0`

    Returns
    -------
    `float`
        The BMI (Body Mass Index)
    """
    weight = weight if weight is not None else 165
    feet = feet if feet is not None else 6
    inches = inches if inches is not None else 0

    total_inches = feet * 12 + inches
    bmi = weight / (total_inches * total_inches) * 703
    return round(bmi, _round_dig)


def bmi_metric(
    weight: float,
    height: float):
    """
    Calculate one's BMI (Body Mass Index) given one's weight and height

    Parameters
    ----------
    `weight` : float or None.
        one's weight in kgs. defaults to `75`\n
    `height` : float or None
        one's height in cms. defaults to `183`

    Returns
    -------
    `float`
        The BMI (Body Mass Index)
    """
    weight = weight if weight is not None else 75
    height = height if height is not None else 183

    bmi = weight / ((height * height) / 10000)
    return round(bmi, _round_dig)
