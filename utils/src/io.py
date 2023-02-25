from glob import glob
from datetime import datetime
import pandas as pd
from config import *


def txt_to_str(fname):
    with open(fname, "r") as file:
        data = file.read().replace("\n", "")
    return data


def read_file_from_symbol(symbol, basedir=str(day_)):
    file = glob(basedir + "/*" + symbol + "*")[0]
    print(file)
    df = pd.read_csv(file)
    df["Date"] = df["date"].apply(
        lambda x: datetime.strptime(x.split(" ")[0], "%Y-%m-%d")
    )
    df.drop(["Unnamed: 0", "date"], inplace=True, axis=1)
    return df


def read_file_from_symbol2(symbol, basedir=str(day_)):
    file = glob(basedir + "/" + symbol + ".csv")[0]
    print(file)
    df = pd.read_csv(file)[["Date", "Open", "High", "Low", "Close", "Volume"]]
    df.columns = ["Date", "open", "high", "low", "close", "volume"]
    df["Date"] = df["Date"].apply(
        lambda x: datetime.strptime(x.split(" ")[0], "%Y-%m-%d")
    )
    # df.drop(['Unnamed: 0'],inplace=True, axis=1)
    return df


def read_file_from_symbol3(symbol, basedir=str(day_)):
    file = glob(basedir + "/*" + symbol + "*")[0]
    print(file)
    df = pd.read_csv(file)
    df["Date"] = df["date"].apply(
        lambda x: datetime.strptime(x.split("+")[0], "%Y-%m-%d %H:%M:%S")
    )
    df.drop(["Unnamed: 0", "date"], inplace=True, axis=1)
    return df


def filter_df_dates(df, start_, end_):
    start_ = datetime.strptime(start_, "%Y%m%d")
    end_ = datetime.strptime(end_, "%Y%m%d")
    Q_df = df[(df["Date"] >= start_) & (df["Date"] <= end_)]
    return Q_df
