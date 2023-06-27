# %%
from datetime import datetime
import os
import pandas as pd
from glob import glob

from ..common.tradingview import *
from ..common.config import *

# %%

# %%
os.chdir(today_wl)

# %%
files = glob("*Mom*.xlsx")
print(files)

# %%
df = pd.read_excel(files[0])
tickers = set(df["Unnamed: 2"])
print(len(tickers))

# %%
bands_url = "https://archives.nseindia.com/content/equities/sec_list.csv"
bands_data = pd.read_csv(bands_url)
ignore_filters = ["2", "5"]
filtered_stocks = bands_data.loc[~bands_data["Band"].isin(ignore_filters)]
filtered_set = set(filtered_stocks["Symbol"])

tickers = tickers.intersection(filtered_set)
print(len(tickers))

# %%
set_to_tv_exchange(tickers, today_blank + "_VCP.txt")

# %%
os.remove(files[0])
