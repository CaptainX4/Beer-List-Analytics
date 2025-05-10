# data_loader.py
import certifi, ssl, urllib.request as urllib2
import numpy as np
import pandas as pd
from io import StringIO

DEFAULT_ADDED_DATE = "11/3/2013"
UNAMERICAN_DROP_COLUMNS = ["Comments", "Country Total", "Zak Total", "Jon Total", "Maps Link"]
AMERICAN_DROP_COLUMNS = ["Comments", "Zipcode"]

def replace_missing_added(df: pd.DataFrame) -> pd.DataFrame:
    df["Added"] = df["Added"].replace(np.nan, DEFAULT_ADDED_DATE)
    return df

def drop_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    return df.drop(columns, axis=1)

def drop_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(how="all")

def load_csv_from_url(url: str) -> pd.DataFrame:
    context = ssl.create_default_context(cafile=certifi.where())
    data = urllib2.urlopen(url, context=context).read()
    data_str = data.decode("utf-8")
    return pd.read_csv(StringIO(data_str))

def clean_unamerican_data(df: pd.DataFrame) -> pd.DataFrame:
    df = replace_missing_added(df)
    df = drop_columns(df, UNAMERICAN_DROP_COLUMNS)
    df = df.dropna(subset=["Brewery"], how='all')
    df = drop_empty_rows(df)
    return df.rename(columns={"Country": "Territory"})

def clean_american_data(df: pd.DataFrame, drop_last_rows: int = 0, subset_filter: str | None = None) -> pd.DataFrame:
    df = replace_missing_added(df)
    df = drop_columns(df, AMERICAN_DROP_COLUMNS)
    for _ in range(drop_last_rows):
        df = df.drop(df.index[-1])
    if subset_filter:
        df = df.dropna(subset=[subset_filter], how='all')
    df = drop_empty_rows(df)
    return df.rename(columns={"State": "Territory"})