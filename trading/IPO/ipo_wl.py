# %%
import pandas as pd
from dateutil import parser
from ..common.config import *
from ..common.tv_utils import *
import os

stocks_data = pd.read_csv(nse_master_url)

stocks_data["ListingDate"] = stocks_data[" DATE OF LISTING"].apply(
    lambda x: parser.parse(x)
)
stocks_data["ListingYear"] = stocks_data["ListingDate"].apply(lambda x: x.year)
years = set(stocks_data["ListingYear"])
grouped = stocks_data.groupby(["ListingYear"])


os.chdir(ipo_wl)
for y in years:
    temp = grouped.get_group(y)
    s = set(temp["SYMBOL"])
    outfile = f"{y}.txt"
    if check_file(outfile):
        continue
    set_to_tv_ind(s, outfile)
