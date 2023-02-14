from pathlib import Path

# paths
trading_ = Path("/Users/yash/Desktop/Trading")
code_ = trading_ / "code"
data_ = trading_ / "historical_data"

# hist. data
minute_ = data_ / "kite_connect/minute"
minute_5 = data_ / "kite_connect/minute_5"
day_ = data_ / "kite_connect/day"
minute_nifty500 = data_ / "kite_connect/nifty_500"
daily_us = data_ / "US/daily"

# TV
tv_wl = trading_ / "tradingview_watchlists"
nifty500_csv = tv_wl / "broad/ind_nifty500list.csv"
nifty500_txt = tv_wl / " broad/NIFTY_500.txt"

# Q
q_wl = trading_ / "Q/watchlists"
q_bwl = trading_ / "Q/backwatchlists"
deepdive = trading_ / "Q/deep_dive"

# VWAP
vwap = trading_ / "VWAP"
vwap_img = vwap / "img"
vwap_wl = vwap / "watchlists"
# VCP
vcp_wl = trading_ / "VCP/watchlists"
