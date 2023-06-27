# %%
import pandas as pd
from glob import glob
from ..common.tradingview import *
from ..common.config import *


while True:
    fname = input("Please Enter Filename:")
    fname = f"{fname}.xlsx"
    if fname in glob("*.xlsx"):
        break
    else:
        print("File not present in folder, please try again!")

df = pd.read_excel(fname)

tickers = set(df["Unnamed: 2"])

bands_url = "https://archives.nseindia.com/content/equities/sec_list.csv"
bands_data = pd.read_csv(bands_url)
ignore_filters = ["2", "5"]
filtered_stocks = bands_data.loc[~bands_data["Band"].isin(ignore_filters)]
filtered_set = set(filtered_stocks["Symbol"])
tickers = tickers.intersection(filtered_set)
print(len(tickers))
set_to_tv_exchange(tickers, f"{today_blank}_{fname.replace('xlsx', 'txt')}")
