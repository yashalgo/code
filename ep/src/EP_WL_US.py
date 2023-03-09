# %%
# for mondays -> previous day does not provide earnings for Friday AMC

# %%
import pandas as pd
from config import *
import os
from datetime import datetime
from finvizfinance.screener.custom import Custom
import utils.tradingview as tv
import utils.misc as msc
import yfinance as yf


# %%
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


# %%
def get_yf_df(symbol, period_="1mo"):
    df2 = yf.download(symbol, period=period_, progress=False)
    df2.rename(columns=str.lower, inplace=True)
    df2.drop("close", axis=1, inplace=True)
    df2.rename(columns={"adj close": "close"}, inplace=True)
    df2.reset_index(inplace=True)
    return df2


# %%
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

fcustom.set_filter(filters_dict=filters_dict1)
df1 = fcustom.screener_view(columns=cols, sleep_sec=1)

fcustom.set_filter(filters_dict=filters_dict2)
df2 = fcustom.screener_view(columns=cols, sleep_sec=1)

df_final = pd.concat([df1, df2], axis=0)
df_final = finviz.standardize(df_final)


# %%
df_final["DollarVolume"] = df_final["Price"] * df_final["Avg Volume"]

# %%
df = get_yf_df("META")
df["Date"] = df["Date"].apply(
    lambda x: datetime.strptime(datetime.strftime(x, "%Y-%m-%d"), "%Y-%m-%d")
)
df = df[df["Date"] < datetime.today()]

# %%
previous_day = datetime.strftime(df.iloc[-1, 0], "%b %d") + "/a"
today_ = datetime.strftime(datetime.today(), "%b %d") + "/b"

# %%
print(previous_day, today_)

# %%
df_final = df_final[
    (df_final["DollarVolume"] >= 1e6)
    & ((df_final["Earnings"] == previous_day) | (df_final["Earnings"] == today_))
]

# %%
print(df_final.shape[0], "\n")

# %%
os.chdir(ep_wl)

# %%
s1 = set(df_final["Ticker"])
# tv.set_to_tv(s1, datetime.today().strftime('%Y%m%d') + '_AMC.txt')

# %%
tv.set_to_tv(s1, datetime.today().strftime("%Y%m%d") + "_EP.txt")
