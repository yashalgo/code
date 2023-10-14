# CONFIGURATION FILE

from pathlib import Path
from datetime import datetime, timedelta

# dates
today = datetime.today() - timedelta(days=0)
today_blank = today.strftime("%Y%m%d")
today_slash = today.strftime("%Y/%m/%d")
today_dash = today.strftime("%Y-%m-%d")

# commom
trading_ = Path("/Users/yash/Desktop/Trading")

code = trading_ / "code/trading"
downloads = Path("/Users/yash/Downloads")

# HIST_DATA
data_ = trading_ / "historical_data"
minute_ = data_ / "kite_connect/minute"
minute_5 = data_ / "kite_connect/minute_5"
day_ = data_ / "kite_connect/day"
minute_nifty500 = data_ / "kite_connect/nifty_500"
daily_us = data_ / "us/daily"
daily_ind = data_ / "india/daily"
daily_us_20y = data_ / "us/20y"
nse_bhavcopy = data_ / "nse_bhavcopy"
stocks = nse_bhavcopy / "stocks"
bhavcopy = nse_bhavcopy / "bhavcopy"

# EP
ep = code / "ep"
ep_data = ep / "data"
bse_earnings_db = ep_data / "Results.csv"

# Q
q = trading_ / "Q"
deepdive = q / "deep_dive"

# backsetups
bs = trading_ / "backsetups"
q_bs_us = bs / "q_bs_us"
q_bs_ind = bs / "q_bs_ind"
ep_bs_us = bs / "ep_bs_us"

# WL
tv_wl = trading_ / "tradingview_watchlists"
wl = trading_ / "watchlists"
bwl = wl / "backwatchlists"
today_wl = wl / today_slash
ipo_wl = tv_wl / "ipo"
earnings_wl = wl / "earnings"

# TV
nifty500_csv = tv_wl / "broad/ind_nifty500list.csv"
nifty500_txt = tv_wl / " broad/NIFTY_500.txt"

# tji
tji = code / "tji"
tji_data = tji / "data"
tji_mm = tji_data / "mm"
tji_figs = tji_data / "figs"

# msi
msi = code / "msi"
msi_data = msi / "data"

msi_raw_data = msi_data / "raw"

msi_ind_grp = msi_data / "ind_grp"
msi_ind_grp_csv = msi_ind_grp / "csv" / f"{today_blank}_ind_grp_ranks.csv"
msi_ind_grp_csv_f = msi_ind_grp / "csv" / f"{today_blank}_ind_grp_ranks_f.csv"
msi_ind_grp_img = msi_ind_grp / "img" / f"{today_blank}_ind_grp.png"
msi_ind_grp_wl = msi_ind_grp / "wl"

SIGN_IN_URL = "https://marketsmithindia.com/mstool/landing.jsp#/signIn"
LANDING_URL = "https://marketsmithindia.com/mstool/landing.jsp#/"
IND_GRP_RANKS = "https://marketsmithindia.com/mstool/industrygrouplist.jsp"
MSI_SCREENER = "https://marketsmithindia.com/mstool/list/build-your-screen/filter-india-stocks/idealists.jsp#/"

# chartink
ci = code / "ci"
ci_data = ci / "data"
ci_top_gainers = today_wl / "Top Gainers.csv"
exchange = code / "exch"
exchange_data = exchange / "data"
nse_bands_txt = exchange_data / f"{today_blank}_nse_bands.txt"
nse_bands_txt_f = exchange_data / f"{today_blank}_nse_bands_f.txt"

bse_master_csv = exchange_data / "bse_master.csv"
bse_results_csv = exchange_data / f"{today_blank}_bse_results.csv"
bse_results_html = f"bse_results_{today_blank}.html"

# bhavcopy
# NSE
nse_bhavcopy = data_ / "nse_bhavcopy"
nse_bhav_dir = nse_bhavcopy / "bhavcopy"
nse_stocks_dir = nse_bhavcopy / "stocks"
nse_stocks_db = nse_stocks_dir / "nse_stocks.db"
nse_list_of_equity = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
nse_bc_url = (
    "https://archives.nseindia.com/content/historical/EQUITIES/{}/{}/cm{}bhav.csv.zip"
)
nse_bands_csv = exchange_data / f"{today_blank}_nse_bands.csv"
nse_master_csv = exchange_data / f"{today_blank}_nse_master.csv"
# BSE
bse_bhavcopy = data_ / "bse_bhavcopy"
bse_bhav_dir = bse_bhavcopy / "bhavcopy"
bse_stocks_dir = bse_bhavcopy / "stocks"
bse_stocks_db = bse_stocks_dir / "bse_stocks.db"
bse_bc_url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ{}_CSV.zip"

# combined
combined_csv = exchange_data / f"{today_blank}_combined_master.csv"

# urls
nse_master_url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
nse_bands_url = "https://archives.nseindia.com/content/equities/sec_list.csv"
bse_master_url = "https://api.bseindia.com/BseIndiaAPI/api/LitsOfScripCSVDownload/w?segment=&status=&industry=&Group=&Scripcode="
bse_results_url = "https://www.bseindia.com/corporates/Forth_Results.html"

msi_login_url = "https://marketsmithindia.com/mstool/landing.jsp#/signIn"
msi_screener_url = "https://marketsmithindia.com/mstool/list/build-your-screen/filter-india-stocks/idealists.jsp#/"

tijori_signin_url = "https://www.tijorifinance.com/account/signin/"
tijori_mm_url = "https://www.tijorifinance.com/in/markets"

# top_gainers_1m = "https://chartink.com/screener/top-gainers-1m"
# top_gainers_3m = "https://chartink.com/screener/top-gainers-3m-3"
# top_gainers_6m = "https://chartink.com/screener/top-gainers-3m-2"
# top_gainers_12m = "https://chartink.com/screener/top-gainers-12m"
# hv = "https://chartink.com/screener/hvq-3"
mom_url = "https://chartink.com/screener/copy-momentum-stocks-initial-scanner-156"
# mom_url = "https://chartink.com/screener/mark-minervini-trend-template-simplified"

bse_bhav_copy_url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ280723_CSV.ZIP"

# chartink
ci = code / "ci"
ci_data = ci / "data"
# ci_login_url = "https://chartink.com/login"

nse_liquid_wl = today_wl / f"{today_blank}_NSE_LIQUID.txt"


# twitter
twitter = code / "twitter"
twitter_data = twitter / "data"

# telegram
tg = code / "tg"

# credentials
cred = trading_ / "code/credentials"
cred_tji = cred / "cred_tji.json"
cred_msi = cred / "cred_msi.json"
cred_ci = cred / "cred_ci.json"
cred_tg_yash = cred / "cred_tg_yash.json"
cred_twitter = cred / "cred_twitter_yash.json"
cred_fv_yash = cred / "cred_fv_yash.json"
cred_fv_mohan = cred / "cred_fv_mohan.json"

# AUTH
AUTH_MOHAN = cred / "auth_mohan.json"
AUTH_YASH = cred / "auth_yash.json"

# SQL
sql = code / "sql"
sql_db = sql / "db"
stocks_data_table = sql_db / "stocks_data.json"

# NIFTY INDICES
# BROAD
nse_indices = exchange_data / "nse_indices"
nifty_indices_base_url = "https://archives.nseindia.com/content/indices/ind_{}list.csv"

nifty_50 = nifty_indices_base_url.format("nifty50")
nifty_nxt_50 = nifty_indices_base_url.format("niftynext50")
nifty_100 = nifty_indices_base_url.format("nifty100")
nifty_200 = nifty_indices_base_url.format("nifty200")
nifty_500 = nifty_indices_base_url.format("nifty500")

nifty_total_market = nifty_indices_base_url.format("niftytotalmarket_")

nifty_midcap_50 = nifty_indices_base_url.format("niftymidcap50")
nifty_midcap_100 = nifty_indices_base_url.format("niftymidcap100")
nifty_midcap_150 = nifty_indices_base_url.format("niftymidcap150")
nifty_midcap_select = nifty_indices_base_url.format("niftymidcapselect_")
nifty_smallcap_50 = nifty_indices_base_url.format("niftysmallcap50")
nifty_smallcap_100 = nifty_indices_base_url.format("niftysmallcap100")
nifty_smallcap_250 = nifty_indices_base_url.format("niftysmallcap250")
nifty_microcap_250 = nifty_indices_base_url.format("niftymicrocap250_")
nifty_large_midcap_250 = nifty_indices_base_url.format("niftylargemidcap250")
nifty_mid_smallcap_400 = nifty_indices_base_url.format("niftymidsmallcap400")

nse_broad_indices = [
    nifty_50,
    nifty_nxt_50,
    nifty_100,
    nifty_200,
    nifty_500,
    nifty_total_market,
    nifty_midcap_50,
    nifty_midcap_100,
    nifty_midcap_150,
    nifty_midcap_select,
    nifty_smallcap_50,
    nifty_smallcap_100,
    nifty_smallcap_250,
    nifty_microcap_250,
    nifty_large_midcap_250,
    nifty_mid_smallcap_400,
]

# SCREENER
screener = code / "screener"
liquid_stocks_url = "https://www.screener.in/screens/1145899/liquid-stocks/"
liquid_stocks_txt = f"{today_blank}_liquid_stocks.txt"
liquid_stocks_f_txt = f"{today_blank}_liquid_stocks_f.txt"
screener_data = screener / "data"
liquid_dir = screener_data / "liquid"
# CHROMEDRIVER
chromedriver_path = trading_ / "code/drivers/chromedriver-mac-arm64/chromedriver"

# mbm
mbm = code / "mbm"
mbm_data = mbm / "data"
mbm_files = mbm_data / "files"
mbm_db = mbm_data / "db"


# GITHUB NSE BREADTH REPO
nse_breadth = trading_ / "code/seed_yashalgo_nse_breadth"
nse_breadth_data = nse_breadth / "data"
nse_breadth_json = nse_breadth / "symbol_info/seed_yashalgo_nse_breadth.json"
