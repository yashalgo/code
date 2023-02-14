# %%
from libs import *
from paths import *
from helper_functions import *
from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
import yfinance as yf

yf.pdr_override()

# %%
# SCREENER
fcustom = Custom()
cols = [0, 1, 2, 3, 4, 6, 43, 44, 45, 51, 52, 53, 63, 65, 68]

vol1 = "Month - Over 5%"
filters_dict1 = {"Market Cap.": "+Micro (over $50mln)", "Volatility": vol1}
fcustom.set_filter(filters_dict=filters_dict1)
df1 = fcustom.screener_view(
    columns=cols, sleep_sec=1, order="Performance (Month)", ascend=False
)
print(df1.shape[0])

# %%
end_date = datetime.today()

# %%
today_ = end_date.strftime("%Y/%m/%d")

# %%
path_ = q_wl / today_
if not os.path.isdir(path_):
    os.mkdir(path_)
os.chdir(path_)
# if not os.path.isdir('temp'):
#     os.mkdir('temp')
# os.chdir('temp')

# %%
os.chdir(daily_us)
files = glob("*.csv")

# %%
tickers = df1["Ticker"]
request_times = []
errors = 0
ticker_df = pd.DataFrame(columns=["Ticker", "1m", "3m", "6m", "DV", "ADR%"])


# %%
def get_yf_df(df2):
    df2.rename(columns=str.lower, inplace=True)
    df2.drop("close", axis=1, inplace=True)
    df2.rename(columns={"adj close": "close"}, inplace=True)
    return df2


# %%
start_time = time.time()
for ticker in tickers:
    try:
        # Download historical data as CSV for each stock (makes the process faster)
        outfile = ticker + ".csv"
        if outfile in files:
            print("Ticker present: ", ticker)
            df = pd.read_csv(outfile)
            df["Date"] = df["Date"].apply(
                lambda x: datetime.strptime(x.split(" ")[0], "%Y-%m-%d")
            )
            while (
                len(request_times) >= 2000
                and (time.time() - request_times[-2000]) < 3600
            ):
                time.sleep(1)
            df2 = yf.download(ticker, start=df["Date"].iloc[-1], end=end_date)
            request_times.append(time.time())
            df2 = get_yf_df(df2)
            df2.reset_index(level=0, inplace=True)
            df2["Date"] = df2["Date"].apply(
                lambda x: datetime.strptime(
                    datetime.strftime(x, "%Y-%m-%d"), "%Y-%m-%d"
                )
            )
            df = pd.concat([df, df2], axis=0)
        else:
            print("Ticker not present: ", ticker)
            while (
                len(request_times) >= 2000
                and (time.time() - request_times[-2000]) < 3600
            ):
                time.sleep(1)
            df = yf.download(ticker, period="6mo")
            request_times.append(time.time())
            df = get_yf_df(df)

        df["DollarVolume"] = df["close"] * df["volume"]
        df.drop_duplicates(subset="Date", inplace=True, keep="first")
        df.reset_index(inplace=True)
        df.drop("index", axis=1, inplace=True)
        df = df[-128:]
        # n-month gains
        adr(df)
        for i in [1, 3, 6]:
            n_month_gain(df, i)
            # print(ticker_df)
        ticker_df.loc[len(ticker_df.index)] = [
            ticker,
            df["1M_low_gain"].iloc[-1],
            df["3M_low_gain"].iloc[-1],
            df["6M_low_gain"].iloc[-1],
            df["DollarVolume"].iloc[-1],
            df["ADR%"].iloc[-1],
        ]
        # print(ticker, df.shape)
        df.to_csv(outfile)
    except:
        print("Error for ticker: ", ticker)
        errors += 1
print("Time taken: {}".format(time.time() - start_time))

# %%
ticker_df = pd.merge(ticker_df, df1, on="Ticker")
ticker_df = ticker_df[
    [
        "Ticker",
        "1m",
        "3m",
        "6m",
        "DV",
        "ADR%",
        "Company",
        "Sector",
        "Industry",
        "Market Cap",
        "Price",
        "Earnings",
    ]
]

# %%
# PARAMETERS
mil = 10**6
adr_filter = 5.0
dv_filter = 1 * mil
limit = 100

# %%
# FILTER
ticker_df_filt = ticker_df[
    (ticker_df["ADR%"] >= adr_filter) & (ticker_df["DV"] >= dv_filter)
]

# %%
# RANK
ticker_df_filt["1m_Rating"] = ticker_df_filt["1m"].rank(ascending=False)
ticker_df_filt["3m_Rating"] = ticker_df_filt["3m"].rank(ascending=False)
ticker_df_filt["6m_Rating"] = ticker_df_filt["6m"].rank(ascending=False)

ticker_df_1m = ticker_df_filt[ticker_df_filt["1m_Rating"] <= limit]
ticker_df_3m = ticker_df_filt[ticker_df_filt["3m_Rating"] <= limit]
ticker_df_6m = ticker_df_filt[ticker_df_filt["6m_Rating"] <= limit]

# %%
ticker_df_final = pd.concat([ticker_df_1m, ticker_df_3m, ticker_df_6m], axis=0)
ticker_df_final = ticker_df_final.drop_duplicates(subset=["Ticker"], keep="first")

# %%
os.chdir(q_wl / today_)

# %%
s1 = set(ticker_df_1m["Ticker"])
set_to_tv(s1, datetime.today().strftime("%Y%m%d") + "_1_M_Q_US.txt")
s3 = set(ticker_df_3m["Ticker"])
set_to_tv(s3, datetime.today().strftime("%Y%m%d") + "_3_M_Q_US.txt")
s6 = set(ticker_df_6m["Ticker"])
set_to_tv(s6, datetime.today().strftime("%Y%m%d") + "_6_M_Q_US.txt")

s = set(ticker_df_final["Ticker"])
set_to_tv(s, datetime.today().strftime("%Y%m%d") + "_Q_US.txt")


# %%
ticker_df_final.to_csv("INFO.csv")

# %%
# shutil.rmtree('temp')
