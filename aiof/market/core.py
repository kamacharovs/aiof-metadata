import warnings
import numpy as np
import pandas as pd

warnings.simplefilter(action="ignore", category=FutureWarning)

import pandas_datareader as pdr
import pandas_datareader.data as web
import datetime
import requests_cache


def get_spy(
    date_from: datetime = None,
    date_to: datetime = None) -> pd.DataFrame:
    """
    Get SPY data within a date range

    Parameters
    ----------
    `date_to` : datetime or None.
        date from which to get finance data. defaults to `datetime.datetime.now()`\n
    `date_from` : datetime or None.
        date to which to get finance data. defaults to `date_to - datetime.timedelta(days=365)`\n
    """
    expire_after = datetime.timedelta(days=3)
    session = requests_cache.CachedSession(cache_name="market-spy", backend="sqlite", expire_after=expire_after)
    date_to = date_to if date_to is not None else datetime.datetime.now()
    date_from = date_from if date_from is not None else date_to - datetime.timedelta(days=365)
    return web.DataReader("spy", "yahoo", date_from, date_to, session=session)
