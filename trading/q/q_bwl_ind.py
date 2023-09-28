# %% [markdown]
# #Creates backwatchlist set for watchlists from last friday to most recent thursday => watchlists for all trading days for last trading week

# %%
from datetime import timedelta
import os
from glob import glob
from ..common.config import *
from ..common.tv_utils import *

# import utils.tradingview as tv

# %%
last_friday = today + timedelta(days=-today.weekday() - 3)
latest_thursday = last_friday + timedelta(days=6)

# %%
print(last_friday, latest_thursday)

# %%
dateset = set()

# %%
for i in range(7):
    d = last_friday + timedelta(days=i)
    ds = d.strftime("%Y%m%d")
    dateset.add(ds)

# %%
os.chdir(wl)

# %%
files = glob("**/????????_Q_IND.txt", recursive=True)

# %%
ticker_set = set()

# %%
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
os.chdir(bwl / "q_ind")

last_friday = last_friday.strftime("%Y%m%d")
latest_thursday = latest_thursday.strftime("%Y%m%d")
outfile = f"{last_friday}_{latest_thursday}_Q_BWL_IND.txt"

# %%
set_to_tv_ind(s=ticker_set, outfile=outfile, print_=True, filter_bands=False)
