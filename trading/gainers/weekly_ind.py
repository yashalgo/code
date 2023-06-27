import os
from glob import glob
from ..common.config import *
from ..common.tradingview import *
import sys

os.chdir(bwl / "weekly_gainers_ind")
outfile = f"{today_blank}_1WG_IND.txt"

files = glob("**/*.*", recursive=True)
if outfile in files:
    print("File already present. Aborting!")
    sys.exit()
filename = f"{today_blank}.xlsx"

if filename in files:
    df = pd.read_excel(filename)
    tickers = set(df["Unnamed: 2"])
else:
    print(f"File missing: {filename}")
    sys.exit()


set_to_tv_exchange(tickers, outfile)

try:
    os.remove(filename)
except:
    pass
