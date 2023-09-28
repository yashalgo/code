import pandas as pd
import os

from ..common.config import *
from ..common.io import *
from ..common.tv_utils import *

change_dir(today_wl)

outfile = today_blank + "_EP_IND_D.txt"
if check_file(outfile):
    print("File already exists")
    exit()

earnings_df = pd.read_csv(bse_earnings_db)
# Convert the "Result Date" column to datetime
earnings_df["Result Date"] = pd.to_datetime(
    earnings_df["Result Date"], format="%d %b %Y"
)


# Get next Monday's date and the following Sunday's date
today_ = pd.Timestamp.now().normalize()
earnings_df = earnings_df[earnings_df["Result Date"] == today_]

# print(earnings_df[earnings_df.columns[1]])
s1 = set(earnings_df[earnings_df.columns[1]])
# print(s1)
set_to_tv_ind(s1, outfile)
