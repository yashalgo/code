from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
from ..common.config import *
from ..common.io import *
from ..common.tv_utils import *
from ..common.chrome_utils import *
from ..exch.exch_utils import *
import os
import sys
from glob import glob

if __name__ == "__main__":
    # check if WL already present

    # os.chdir(downloads / "tv")
    # tv_files = glob("*.csv")
    # os.chdir(downloads)
    # files = glob("*.csv")
    # print(len(files))
    # i = 0
    # for f in files:
    #     print(i)
    #     industry_group = f.split("_IN")[0]
    #     tv_file = f"{industry_group}.txt"
    #     if tv_file in tv_files:
    #         continue
    #     print(industry_group)
    #     df = pd.read_csv(f, index_col=False)
    #     # print(df.head())
    #     # break
    #     s = set(df["Symbol"])
    #     # print(len(s))
    #     os.chdir(downloads / "tv")
    # set_to_tv_ind(s, tv_file)
    #     os.chdir(downloads)
    #     i += 1
    #     print("=========")
    #     # break

    os.chdir("/Users/yash/Desktop/Trading/msi")
    df = pd.read_csv("Ind_Grp_raw.csv", index_col=False)
    df["TV_TICKER"] = df["Symbol"].apply(lambda x: get_tv_ticker(x))
    df.to_csv("ind_grp_master_list.csv")
    print(df.head())
