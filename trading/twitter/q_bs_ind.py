# %%
import os
from glob import glob
from datetime import date, timedelta
import shutil

from ..common.config import *

# %%
os.chdir(q_bs_ind)

# %%
latest_monday = today + timedelta(days=-today.weekday())
latest_friday = latest_monday + timedelta(days=4)
print(latest_monday, latest_friday)

# %%
datelist = []
datelist2 = []
for i in range(5):
    d = latest_monday + timedelta(days=i)
    datelist += [d.strftime("%Y-%m-%d")]
    datelist2 += [d.strftime("%d %b")]

# %%
file_set = dict()

folder_name = f"{datelist[0].replace('-','')}_{datelist[-1].replace('-','')}"
try:
    os.mkdir(folder_name)
except:
    pass

for i in datelist:
    files = glob(f"*_{i}.png", recursive=True)
    # print(i, files)
    for j in files:
        shutil.move(j, f"{folder_name}/{j}")
    file_set[i] = files

s = f"""{datelist2[0]} - {datelist2[-1]} [IND]
High Tight Flag | Wedges | Continuation Pocket Pivots    

Actionable Setups from the watchlist::

"""

total = 0
k = 0
for i, j in file_set.items():
    total += len(j)
    s += f"{datelist2[k]}: {len(j)}\n"
    # print(i, len(j))
    k += 1

s += f"""
----------
Total: {total}"""

print(s)
