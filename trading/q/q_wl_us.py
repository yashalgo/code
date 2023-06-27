import pandas as pd
import os
from glob import glob
from datetime import datetime
import sys

import yfinance as yf
import time

from ..common.config import *
from ..common.tradingview import *
from ..common.indicators import *
from ..common.io import *

from finvizfinance.screener.custom import Custom
from pandas_datareader import data as pdr

print(f"Starting program: {sys.argv[0]} at {datetime.now().time()}")
yf.pdr_override()
pd.options.mode.chained_assignment = None  # default='warn'

if not os.path.isdir(today_wl):
    os.mkdir(today_wl)
os.chdir(today_wl)

final_outfile = today_blank + "_Q_US.txt"

if final_outfile in glob("*US*"):
    print("File already exists")
    exit()

# SCREENER
fcustom = Custom()
cols = [0, 1, 2, 3, 4, 6, 43, 44, 45, 51, 52, 53, 63, 65, 68]

vol1 = "Month - Over 3%"
perf1 = "Month Up"
mcap = "+Micro (over $50mln)"
price = "Over $1"
sma50 = "Price above SMA50"
avgvol = "Over 100K"
filters_dict1 = {
    "Market Cap.": mcap,
    "Volatility": vol1,
    "Performance": perf1,
    "Price": price,
    "50-Day Simple Moving Average": sma50,
    "Average Volume": avgvol,
}

isFiltered = False
if not isFiltered:
    fcustom.set_filter(filters_dict=filters_dict1)
    df1 = fcustom.screener_view(
        columns=cols, sleep_sec=1, order="Performance (Month)", ascend=False
    )
    print(df1.shape[0])

    # %%
    df1.to_csv("US_STOCKS.csv")
else:
    df1 = pd.read_csv("US_STOCKS.csv")

# %%
os.chdir(daily_us)
files = glob("*.csv")

# %%
for f in files:
    if today_blank not in f:
        print("Deleting: ", f)
        os.remove(f)

# %%
tickers = df1["Ticker"]
request_times = []
errors = 0
ticker_df = pd.DataFrame(columns=["Ticker", "1m", "3m", "6m", "ADV", "ADR%"])

# %%
start_time = time.time()
for ticker in tickers:
    # print(ticker)
    # try:
    if not isinstance(ticker, str):
        print(f"Not a ticker {ticker}")
        continue

    outfile = ticker + "_" + today_blank + ".csv"
    if outfile in files:
        print("Ticker present: ", ticker)
        df = pd.read_csv(outfile)
    else:
        # API LIMIT
        while (
            len(request_times) >= 2000 and (time.time() - request_times[-2000]) < 3600
        ):
            print("here")
            time.sleep(1)

        df = yf.download(ticker, period="6mo", progress=False)
        request_times.append(time.time())
        df = convert_yf_df(df)
        # ADD TAs
        adv_period = 20
        df["AvgVolume"] = df["volume"].rolling(adv_period).mean()
        df["AvgDollarVolume"] = df["close"] * df["AvgVolume"]
        adr(df)
        for i in [1, 3, 6]:
            n_month_gain(df, i)

    last_row = df.iloc[-1]
    ticker_df.loc[len(ticker_df.index)] = [
        ticker,
        last_row["1M_low_gain"],
        last_row["3M_low_gain"],
        last_row["6M_low_gain"],
        last_row["AvgDollarVolume"],
        last_row["ADR%"],
    ]
    df.to_csv(outfile)
    # except:
    #     print("Error for ticker: ", ticker)
    #     errors += 1
print("Time taken: {}".format(time.time() - start_time))

# %%
ticker_df = pd.merge(ticker_df, df1, on="Ticker")
ticker_df = ticker_df[
    [
        "Ticker",
        "1m",
        "3m",
        "6m",
        "ADV",
        "ADR%",
        "Company",
        "Sector",
        "Industry",
        "Market Cap",
        "Price",
        "Earnings",
    ]
]

# %%
# PARAMETERS
mil = 10**6
adr_filter = 5.0
dv_filter = 3 * mil
limit = 100

# %%
# FILTER
ticker_df_filt = ticker_df[
    (ticker_df["ADR%"] >= adr_filter) & (ticker_df["ADV"] >= dv_filter)
]

# %%
# RANK
ticker_df_filt["1m_Rating"] = ticker_df_filt["1m"].rank(ascending=False)
ticker_df_filt["3m_Rating"] = ticker_df_filt["3m"].rank(ascending=False)
ticker_df_filt["6m_Rating"] = ticker_df_filt["6m"].rank(ascending=False)

ticker_df_1m = ticker_df_filt[ticker_df_filt["1m_Rating"] <= limit]
ticker_df_3m = ticker_df_filt[ticker_df_filt["3m_Rating"] <= limit]
ticker_df_6m = ticker_df_filt[ticker_df_filt["6m_Rating"] <= limit]

# %%
print(ticker_df_1m.shape[0])
print(ticker_df_3m.shape[0])
print(ticker_df_6m.shape[0])

# %%
ticker_df_final = pd.concat([ticker_df_1m, ticker_df_3m, ticker_df_6m], axis=0)
ticker_df_final = ticker_df_final.drop_duplicates(subset=["Ticker"], keep="first")

# %%
os.chdir(today_wl)

# %%
s1 = set(ticker_df_1m["Ticker"])
set_to_tv(s1, today_blank + "_1_M_Q_US.txt")
s3 = set(ticker_df_3m["Ticker"])
set_to_tv(s3, today_blank + "_3_M_Q_US.txt")
s6 = set(ticker_df_6m["Ticker"])
set_to_tv(s6, today_blank + "_6_M_Q_US.txt")

s = set(ticker_df_final["Ticker"])
set_to_tv(s, final_outfile)
