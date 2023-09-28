import pandas as pd
import os

from ..common.config import *
from ..common.io import *
from ..common.tv_utils import *

change_dir(today_wl)

outfile = today_blank + "_EP_IND_W.txt"
if check_file(outfile):
    print("File already exists")
    exit()

earnings_df = pd.read_csv(bse_earnings_db)
# Convert the "Result Date" column to datetime
earnings_df["Result Date"] = pd.to_datetime(
    earnings_df["Result Date"], format="%d %b %Y"
)


# Get next Monday's date and the following Sunday's date
next_monday = pd.Timestamp.now().normalize() + pd.DateOffset(
    days=(7 - pd.Timestamp.now().dayofweek + 1 - 1) % 7
)

next_sunday = next_monday + pd.DateOffset(days=4)

print(next_monday, next_sunday)
# Filter rows where "Result Date" is between next Monday and the following Sunday
earnings_df = earnings_df[
    (earnings_df["Result Date"] >= next_monday)
    & (earnings_df["Result Date"] <= next_sunday)
]

# Print the filtered DataFrame
# print(earnings_df)


print(earnings_df[earnings_df.columns[1]])
s1 = set(earnings_df[earnings_df.columns[1]])

set_to_tv_ind(s1, outfile)
