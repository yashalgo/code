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


def adr(df, period=20):
    df["ADR%"] = ((df["high"] / df["low"]).rolling(period).mean() - 1) * 100
    return df


def n_month_gain(df, n):
    col_name = str(n) + "M_low"
    df[col_name] = df["low"].rolling(min(126, n * 22)).min()
    # print(df.head())
    col_name2 = col_name + "_gain"
    df[col_name2] = (df["close"] / df[col_name] - 1) * 100
    df.drop(col_name, inplace=True, axis=1)
    return df


def add_ma(df, n):
    col_name = "DMA" + str(n)
    df[col_name] = df["close"].rolling(n).mean()
    return df
