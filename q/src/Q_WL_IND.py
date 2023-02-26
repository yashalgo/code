# %%
from datetime import date, timedelta, datetime
import os
from glob import glob
from config import *
import utils.tradingview as tv
import pandas as pd

# %%
today = datetime.today().strftime("%Y/%m/%d")

# %%
os.chdir(q_wl / today)

# %%
files = glob("?.xlsx")
print(files)

# %%
# 1-3-6 m gainers

s = set()

for i in [1, 3, 6]:
    df = pd.read_excel(str(i) + ".xlsx")
    print(df["Unnamed: 2"].shape[0])
    temp_set = set(df["Unnamed: 2"])
    tv.set_to_tv(
        temp_set, outfile=today.replace("/", "") + "_" + str(i) + "_M_Q_IND.txt"
    )
    s.update(temp_set)
print(len(s))
tv.set_to_tv(s, today.replace("/", "") + "_Q_IND.txt")
