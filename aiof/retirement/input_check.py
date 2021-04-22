def float_check(
    parameter_value: float,
    parameter_name: str):
    """
    Perform basic parameter checks for a `float` parameter. This ranges from checking for `None`, negative values, etc.

    Parameters
    ----------
    `parameter_value` : float
        the parameter's value\n
    `parameter_name` : str
        the parameter's name
    """
    if (parameter_value is None):
        raise ValueError(f"{parameter_name} cannot be None")
    elif (parameter_value < 0):
        raise ValueError(f"{parameter_name} cannot be negative")
    
def age_check(
    parameter_value: int,
    parameter_name: str):
    """
    Perform basic parameter checks for an age `int` parameter. This ranges from checking for `None`, negative values, bigger than, etc.

    Parameters
    ----------
    `parameter_value` : int
        the parameter's value. in terms of a person's age\n
    `parameter_name` : str
        the parameter's name
    """
    if (parameter_value is None):
        raise ValueError(f"{parameter_name} cannot be None")
    elif (parameter_value <= 0):
        raise ValueError(f"{parameter_name} cannot be zero or negative")
    elif (parameter_value > 120):
        raise ValueError(f"{parameter_name} is bigger than 120")