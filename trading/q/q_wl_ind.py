import os
from glob import glob
from ..common.config import *
from ..common.tv_utils import *
import pandas as pd

# find all images without alternate text and give them a red border


if __name__ == "__main__":
    path_ = os.path.abspath(today_wl)
    # print(path_)
    if not os.path.exists(today_wl):
        os.makedirs(today_wl)
    os.chdir(today_wl)

    files = glob("*.xlsx")
    print(files)

    s = set()

    for i in [1, 3, 6, 12]:
        df = pd.read_excel(str(i) + ".xlsx")
        temp_set = set(df["Unnamed: 2"])
        s.update(temp_set)

    set_to_tv_ind(s, today_blank + "_Q_IND.txt")

    for f in files:
        os.remove(f)
