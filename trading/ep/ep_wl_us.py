import pandas as pd
import os
from datetime import datetime, timedelta
from finvizfinance.screener.custom import Custom
import yfinance as yf

from ..common.config import *
from ..common.io import *
from ..common.tradingview import *


class finviz:
    mcap_50 = "+Micro (over $50mln)"

    earnings_prev5 = "Previous 5 Days"
    earnings_next5 = "Next 5 Days"
    earnings_amc = "Yesterday After Market Close"
    earnings_bmo = "Today Before Market Open"

    country_usa = "USA"

    price_1 = "Over $1"

    def standardize(df1):
        df1["Market Cap"] = df1["Market Cap"] / 1e6
        df1["Float"] = df1["Float"] / 1e6
        df1["Volatility M"] = df1["Volatility M"] * 100
        df1["Perf Quart"] = df1["Perf Quart"] * 100
        df1["Inst Own"] = df1["Inst Own"] * 100
        return df1


# SCREENER
fcustom = Custom()
cols = [0, 1, 2, 3, 4, 6, 16, 22, 23, 25, 28, 31, 44, 51, 57, 58, 63, 65, 68]

filters_dict1 = {
    "Market Cap.": finviz.mcap_50,
    "Earnings Date": finviz.earnings_prev5,
    "Price": finviz.price_1,
    "Country": finviz.country_usa,
}
filters_dict2 = {
    "Market Cap.": finviz.mcap_50,
    "Earnings Date": finviz.earnings_next5,
    "Price": finviz.price_1,
    "Country": finviz.country_usa,
}

if not os.path.isdir(today_wl):
    os.mkdir(today_wl)
os.chdir(today_wl)

outfile = today_blank + "_EP_US.txt"
if outfile in glob("*US*"):
    print("File already exists")
    exit()


fcustom.set_filter(filters_dict=filters_dict1)
df1 = fcustom.screener_view(columns=cols, sleep_sec=1)

fcustom.set_filter(filters_dict=filters_dict2)
df2 = fcustom.screener_view(columns=cols, sleep_sec=1)

df_final = pd.concat([df1, df2], axis=0)
df_final = finviz.standardize(df_final)

df_final["DollarVolume"] = df_final["Price"] * df_final["Avg Volume"]

df = get_yf_df("^IXIC")
df["Date"] = df["Date"].apply(
    lambda x: datetime.strptime(datetime.strftime(x, "%Y-%m-%d"), "%Y-%m-%d")
)
df = df[df["Date"] < today]

previous_day = df.iloc[-1, 0]

previous_day_str = datetime.strftime(previous_day, "%b %d") + "/a"
today_str = datetime.strftime(today, "%b %d") + "/b"

print(previous_day_str, today_str)


df_final = df_final[
    (df_final["DollarVolume"] >= 1e6)
    & ((df_final["Earnings"] == previous_day_str) | (df_final["Earnings"] == today_str))
]

s1 = set(df_final[df_final.columns[0]])

set_to_tv(s1, outfile)
