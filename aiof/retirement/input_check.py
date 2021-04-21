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
    