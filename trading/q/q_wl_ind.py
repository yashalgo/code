# %%
from datetime import datetime, timedelta
import os
from glob import glob
from ..common.config import *
from ..common.tradingview import *
import pandas as pd

os.chdir(today_wl)

# %%
files = glob("?.xlsx")
print(files)

# %%
bands_url = "https://archives.nseindia.com/content/equities/sec_list.csv"
bands_data = pd.read_csv(bands_url)
ignore_filters = ["2", "5"]
filtered_stocks = bands_data.loc[~bands_data["Band"].isin(ignore_filters)]
filtered_set = set(filtered_stocks["Symbol"])

s = set()

for i in [1, 3, 6]:
    df = pd.read_excel(str(i) + ".xlsx")
    temp_set = set(df["Unnamed: 2"])
    temp_set = temp_set.intersection(filtered_set)
    print(len(temp_set))
    set_to_tv_exchange(temp_set, outfile=today_blank + "_" + str(i) + "_M_Q_IND.txt")
    s.update(temp_set)

# %%
print(len(s))
set_to_tv_exchange(s, today_blank + "_Q_IND.txt")

# %%
for f in files:
    os.remove(f)
