# Creates backwatchlist set for watchlists from monday to friday => watchlists for all trading days for last trading week

from datetime import date, timedelta, datetime
import os
from glob import glob
from ..common.config import *
from ..common.tv_utils import *

latest_monday = today + timedelta(days=-today.weekday())
latest_friday = latest_monday + timedelta(days=4)
print(latest_monday, latest_friday)

# %%
dateset = set()

for i in range(5):
    d = latest_monday + timedelta(days=i)
    ds = d.strftime("%Y%m%d")
    dateset.add(ds)

os.chdir(wl)

# %%
# files = glob("**/*US.txt", recursive=True)
files = glob("**/????????_Q_US.txt", recursive=True)

# %%
ticker_set = set()

for f in files:
    ds = f.split("/")[-1].split("_")[0]
    if ds in dateset:
        print(ds)
        with open(f, "r") as file:
            data = file.read().replace("\n", "")
        data = data.split(",")
        ticker_set.update(set(data))
print(len(ticker_set))

# %%
os.chdir(bwl / "q_us")

latest_monday = latest_monday.strftime("%Y%m%d")
latest_friday = latest_friday.strftime("%Y%m%d")
outfile = f"{latest_monday}_{latest_friday}_Q_BWL_US.txt"

set_to_tv_ind(ticker_set, outfile)
