# data_loader.py
import certifi, ssl, urllib.request as urllib2
import pandas as pd
from io import StringIO

def load_csv_from_url(url):
    context = ssl.create_default_context(cafile=certifi.where())
    data = urllib2.urlopen(url, context=context).read()
    data_str = data.decode("utf-8")
    return pd.read_csv(StringIO(data_str))

def clean_unamerican_data(df):
    cleanup_columns = ["Comments", "Country Total", "Zak Total", "Jon Total", "Maps Link"]
    df = df.drop(cleanup_columns, axis=1)
    df = df[~df["Country"].isin(["US", "Total: this sheet", "Total: all sheets"])]
    df = df.dropna(how="all")
    return df.rename(columns={"Country": "Territory"})

def clean_american_data1(df):
    cleanup_columns = ["Comments", "Zipcode"]
    df = df.drop(cleanup_columns, axis=1)
    df = df.drop(df.index[-1])
    df = df.dropna(how = "all")
    return df.rename(columns = {"State": "Territory"})

def clean_american_data2(df):
    cleanup_columns = ["Comments", "Zipcode"]
    df = df.drop(cleanup_columns, axis=1)
    df = df.drop(df.index[0])
    df = df.drop(df.index[-1])
    df = df.drop(df.index[-1])
    df = df.dropna(how="all")
    return df.rename(columns={"State": "Territory"})