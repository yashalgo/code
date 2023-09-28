### TECHNICAL INDICATORS

import pandas as pd


def check_vols(df):
    if max(df.volume) <= 0:
        return False
    return True


def typical_vwap(df):
    q = df.volume.values
    p = df.tp.values
    return df.assign(typical_vwap=(p * q).cumsum() / q.cumsum())


def vwap(df):
    q = df.quantity.values
    p = df.price.values
    return df.assign(vwap=(p * q).cumsum() / q.cumsum())


def n_month_gain(df, n):
    col_name = str(n) + "M_low"
    df[col_name] = df["low"].rolling(min(df.shape[0], n * 22)).min()
    # print(df.head())
    col_name2 = col_name + "_gain"
    df[col_name2] = (df["close"] / df[col_name] - 1) * 100
    df.drop(col_name, inplace=True, axis=1)
    return df


def adr(df, period=20):
    df["ADR%"] = ((df["high"] / df["low"]).rolling(period).mean() - 1) * 100
    return df["ADR"]


def calculate_gain(df, period=21, uppercase=True):
    if len(df) < period:
        return float("nan")
    low = "LOW"
    close = "CLOSE"
    if not uppercase:
        low, close = low.lower(), close.lower()
    lowest_low = min(df[low].iloc[-period:])
    latest_close = df[close].iloc[-1]
    # min_last_period = df[low].shift(1).rolling(window=period).min()
    temp = (latest_close / lowest_low - 1) * 100
    if latest_close < lowest_low:
        print(df["symbol"].iloc[0], lowest_low, latest_close, temp)
        pass
    return temp


###
def calculate_ema(df, period=10, uppercase=True):
    if len(df) < period:
        return float("nan")
    close = "CLOSE"
    if not uppercase:
        close = close.lower()
    temp = df[close].ewm(span=period, adjust=False).mean()
    return temp.iloc[-1]


# Calculate Avg Turnover
def calculate_avg_turnover(df, period=50, uppercase=True):
    if len(df) < period:
        return float("nan")
    turnover = "TURNOVER"
    if not uppercase:
        turnover = turnover.lower()
    return df[turnover].rolling(window=period).mean().iloc[-1]


# Calculate Distance from 52W High/Low
def calculate_distance_from_high(df, period=252, uppercase=True):
    if len(df) < period:
        return float("nan")

    high = "HIGH"
    close = "CLOSE"

    if not uppercase:
        high, close = high.lower(), close.lower()
    df["52W_High"] = df[high].rolling(window=period).max()
    temp = (df[close] - df["52W_High"]) / df["52W_High"] * 100
    df.drop(columns=["52W_High"], inplace=True)
    return temp.iloc[-1]


def calculate_distance_from_low(df, period=252, uppercase=True):
    if len(df) < period:
        return float("nan")

    low = "LOW"
    close = "CLOSE"

    if not uppercase:
        low, close = low.lower(), close.lower()
    df["52W_Low"] = df[low].rolling(window=period).min()
    temp = (df[close] - df["52W_Low"]) / df["52W_Low"] * 100
    df.drop(columns=["52W_Low"], inplace=True)
    return temp.iloc[-1]


def calculate_adr(df, period=20, uppercase=True):
    if len(df) < period:
        return float("nan")
    high = "HIGH"
    low = "LOW"
    if not uppercase:
        high, low = high.lower(), low.lower()
    temp = ((df[high] / df[low]).rolling(period).mean() - 1) * 100
    return temp.iloc[-1]


def calculate_atr(df, period=14, uppercase=True):
    if len(df) < period:
        return float("nan")
    high = "HIGH"
    low = "LOW"
    close = "CLOSE"
    if not uppercase:
        high, low, close = high.lower(), low.lower(), close.lower()
    df["h-l"] = abs(df[high] - df[low])
    df["h-pc"] = abs(df[high] - df[close].shift(1))
    df["l-pc"] = abs(df[low] - df[close].shift(1))
    df["tr"] = df[["h-l", "h-pc", "l-pc"]].max(axis=1)
    df["atr"] = df["tr"].rolling(window=period).mean()
    df.drop(columns=["h-l", "h-pc", "l-pc", "tr"], inplace=True)
    return df["atr"].iloc[-1]
