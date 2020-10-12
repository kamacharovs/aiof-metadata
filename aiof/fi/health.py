import math
import numpy_financial as npf
import pandas as pd

import aiof.config as config


# Configs
_settings = config.get_settings()


# Staying fit and healthy for a longer & better retirement

def bmi_imperial(
    weight,
    feet,
    inches):
    weight = weight if weight is not None else 165
    feet = feet if feet is not None else 6
    inches = inches if inches is not None else 0

    inches = feet * 12 + inches
    bmi = weight / (inches * inches) * 703

    return bmi
