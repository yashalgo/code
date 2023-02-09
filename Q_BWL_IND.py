# #Creates backwatchlist set for watchlists from last friday to most recent thursday => watchlists for all trading days for last trading week

from libs import *
from helper_functions import *
from paths import *

today = date.today()
last_friday = today + timedelta(days=-today.weekday())

print(today, last_friday)

dateset = set()

for i in range(7):
    d = last_friday + timedelta(days=i)
    ds = d.strftime("%Y%m%d")
    dateset.add(ds)

os.chdir(q_wl)

files = glob("**/????????_Q_IND.txt", recursive=True)

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

os.chdir(q_bwl)

set_to_tv(
    ticker_set,
    last_friday.strftime("%Y%m%d") + "_" + today.strftime("%Y%m%d") + "_BWL_IND.txt",
)
