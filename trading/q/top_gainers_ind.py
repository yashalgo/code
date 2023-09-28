import pandas as pd
from ..ci.db import *
from ..ci.ci_utils import *
from ..common.config import *
from ..common.io import *
import sys
import warnings

warnings.simplefilter(action="ignore", category=pd.errors.SettingWithCopyWarning)
OUTFILE = f"{today_blank}_mom_ind.txt"


def process_stocks(file_path, adr_threshold=3.5, n=100):
    # 1. Reading the CSV file
    if not get_top_gainers():
        print("Error getting top gainers")
        return
    print(file_path)
    df = pd.read_csv(file_path)

    # 2. Filtering stocks by adr%
    df_filtered = df[df["adr%"] > adr_threshold]
    # 3. Ranking stocks
    for col in ["gain21", "gain63", "gain126", "gain252"]:
        df_temp = df_filtered.dropna(subset=[col])
        df_filtered[col + "_rank"] = df_temp[col].rank(ascending=False)

    superset = set()
    # 4. Selecting top n stocks for each ranking
    for col in ["gain21", "gain63", "gain126", "gain252"]:
        top_n = set(df_filtered.nsmallest(n, col + "_rank")["symbol"])
        # print(len(top_n))
        # print(top_n)
        superset.update(top_n)
        # print("------")
        # superset = pd.merge(superset, top_n, on="symbol", how="outer")
    df_filtered = df_filtered[df_filtered["symbol"].isin(superset)]
    return df_filtered, superset


if check_file(OUTFILE, today_wl):
    print(f"{OUTFILE} already present. Exiting")
    sys.exit()
df_filtered, superset = process_stocks(ci_top_gainers)


change_dir(today_wl)
df_filtered.to_csv(f"{today_blank}_mom_ind.csv")
os.remove("Top Gainers.csv")
set_to_tv_ind(superset, OUTFILE)
