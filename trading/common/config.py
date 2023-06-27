from pathlib import Path
from datetime import datetime, timedelta

# paths
trading_ = Path("/Users/yash/Desktop/Trading")
code = trading_ / "code/trading"

# AUTH
AUTH_FILE = code / "totp/auth.json"

# HIST_DATA
data_ = trading_ / "historical_data"

minute_ = data_ / "kite_connect/minute"
minute_5 = data_ / "kite_connect/minute_5"
day_ = data_ / "kite_connect/day"
minute_nifty500 = data_ / "kite_connect/nifty_500"
daily_us = data_ / "us/daily"
daily_ind = data_ / "ind/daily"
daily_us_20y = data_ / "us/20y"

# EP
ep = trading_ / "EP"
ep_wl = ep / "watchlists"
ep_data_fh = ep / "finnhub"
gap_data = ep / "gap_final"

# TV
tv_wl = trading_ / "tradingview_watchlists"
nifty500_csv = tv_wl / "broad/ind_nifty500list.csv"
nifty500_txt = tv_wl / " broad/NIFTY_500.txt"

# Q
q = trading_ / "Q"
deepdive = q / "deep_dive"

# backsetups
bs = trading_ / "backsetups"
q_bs_us = bs / "q_bs_us"
q_bs_ind = bs / "q_bs_ind"
ep_bs_us = bs / "ep_bs_us"

# dates
today = datetime.today() - timedelta(days=0)
today_slash = today.strftime("%Y/%m/%d")
today_blank = today.strftime("%Y%m%d")

# WL
wl = trading_ / "watchlists"
bwl = wl / "backwatchlists"

today_wl = wl / today_slash
