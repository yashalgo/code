# %%
import pandas as pd
from pprint import pprint
from bsedata.bse import BSE
import os
from glob import glob
import sys
from datetime import datetime, timedelta, date
from path import Path
import time

from ..common.config import *
from ..common.indicators import *
from ..common.tradingview import *


# %%
print(f"Starting program: {sys.argv[0]} at {datetime.now().time()}")

# %%

# change
# wl = Path("/Users/yash/Desktop/Trading/watchlists/")

if not os.path.isdir(today_wl):
    os.mkdir(today_wl)
os.chdir(today_wl)

# %%
final_outfile = today_blank + "_Q_IND_BSE.txt"

# %%
if final_outfile in glob("*IND*"):
    print("File already exists")
    exit()

# %%
# change
# daily_ind = Path("/Users/yash/Desktop/Trading/historical_data/ind/daily/")

os.chdir(daily_ind)
files = glob("*.csv")

# %%
for f in files:
    if today_blank not in f:
        print("Deleting: ", f)
        os.remove(f)

# %%
b = BSE()
print(b)
b = BSE(update_codes=True)
scrips = b.getScripCodes()
print(f"Number of tickers in BSE: {len(scrips)}")

# %%
tickers = scrips.keys()
request_times = []
errors = 0
ticker_df = pd.DataFrame(columns=["Ticker", "1m", "3m", "6m", "ADV", "ADR%"])


# %%
def getHistoricalDataBSE(ticker, period="6M"):
    his = b.getPeriodTrend(ticker, period)
    df = pd.DataFrame(his)
    df.rename(columns={"date": "Date", "value": "close", "vol": "volume"}, inplace=True)
    df["Date"] = df["Date"].apply(
        lambda x: datetime.strptime(x, "%a %b %d %Y %H:%M:%S").strftime("%d-%m-%Y")
    )
    return df


# %%
start_time = time.time()
for ticker in tickers:
    # print(ticker)
    # try:
    if not isinstance(ticker, str):
        print(f"Not a ticker {ticker}")
        continue

    outfile = ticker + "_" + today_.replace("/", "") + ".csv"
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

        df = getHistoricalDataBSE(ticker)
        request_times.append(time.time())
        # ADD TAs
        adv_period = 20
        df["AvgVolume"] = df["volume"].rolling(adv_period).mean()
        df["AvgDollarVolume"] = df["close"] * df["AvgVolume"]
        # change
        # adr(df)
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
# PARAMETERS
cr = 10**7
adr_filter = 3.5
dv_filter = 5 * cr
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
set_to_tv(s1, today.strftime("%Y%m%d") + "_1_M_Q_IND_BSE.txt")
s3 = set(ticker_df_3m["Ticker"])
set_to_tv(s3, today.strftime("%Y%m%d") + "_3_M_Q_IND_BSE.txt")
s6 = set(ticker_df_6m["Ticker"])
set_to_tv(s6, today.strftime("%Y%m%d") + "_6_M_Q_IND_BSE.txt")

s = set(ticker_df_final["Ticker"])
set_to_tv(s, final_outfile)