# %%
from datetime import datetime
import os
from glob import glob
from common.config import *
import utils.tradingview as tv
from finvizfinance.screener.custom import Custom
import pandas as pd

# %%
fcustom = Custom()

# %%
if not os.path.isdir(today_wl):
    os.mkdir(today_wl)
os.chdir(today_wl)

# %%

# In[4]:
outfile_ = today_blank + "_US.txt"
files = glob("**/*_US.txt", recursive=True)
print(files)
if outfile_ in files:
    print("File already present. Aborting!")
    exit()

# %%
limit = 50

# 1-month performance
perf1 = "Month +30%"
vol1 = "Month - Over 5%"

# 3-month performance
perf3 = "Quarter +50%"
vol3 = "Month - Over 5%"

# 6-month performance
perf6 = "Half +100%"
vol6 = "Month - Over 5%"

cols = [0, 1, 2, 3, 4, 6, 43, 44, 45, 51, 52, 53, 63, 65, 68]

filters_dict1 = {
    "Market Cap.": "+Micro (over $50mln)",
    "Performance": perf1,
    "Price": "Over $1",
    "Volatility": vol1,
    "Average Volume": "Over 100K",
}

filters_dict3 = filters_dict1.copy()
filters_dict3["Performance"] = perf3
filters_dict3["Volatility"] = vol3

filters_dict6 = filters_dict1.copy()
filters_dict6["Performance"] = perf6
filters_dict6["Volatility"] = vol6

# %% [markdown]
# --------------1 MONTH GAINERS-------------

# %%
fcustom.set_filter(filters_dict=filters_dict1)
df1 = fcustom.screener_view(
    columns=cols, sleep_sec=1, order="Performance (Month)", ascend=False
)
print(df1.shape[0])
df1 = df1.head(limit)

df1.shape[0]

# %% [markdown]
# --------------3 MONTH GAINERS-------------

# %%
fcustom.set_filter(filters_dict=filters_dict3)
df3 = fcustom.screener_view(
    columns=cols, sleep_sec=1, order="Performance (Quarter)", ascend=False
)
print(df3.shape[0])
df3 = df3.head(limit)

df3.shape[0]

# %% [markdown]
# --------------6 MONTH GAINERS-------------

# %%
fcustom.set_filter(filters_dict=filters_dict6)
df6 = fcustom.screener_view(
    columns=cols, sleep_sec=1, order="Performance (Half Year)", ascend=False
)
print(df6.shape[0])

df6 = df6.head(limit)

df6.shape[0]

# %% [markdown]
# --------------MERGE-------------

# %%
df_final = pd.concat([df1, df3, df6], axis=0)

# %%
df_final = df_final.drop_duplicates(subset=["Ticker"], keep="first")

# %%
df_final.shape[0]

# %%
s = set(df_final["Ticker"])

# %%
tv.set_to_tv(s, today_blank + "_Q_US.txt")
