from ..common.config import *
from ..common.tv_utils import *
from ..exch.exch_utils import *
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

if __name__ == "__main__":
    df = get_bse_earnings()

    # print(df.head())
    df["Date"] = pd.to_datetime(df["Date"])
    today = datetime.strptime("2023-07-30", "%Y-%m-%d")
    print(today)
    next_week = today + timedelta(weeks=1)
    df_next_week = df[(df["Date"] > today) & (df["Date"] <= next_week)]
    unique_dates = df_next_week["Date"].unique()

    dfs = {date: df_next_week[df_next_week["Date"] == date] for date in unique_dates}

    os.chdir(earnings_wl)
    for date, df in dfs.items():
        print(f"Date: {date}")
        # print(f"Dataframe for this date:\n{df}\n")
        s = set(df["ID"])
        set_to_tv_ind(
            s,
            outfile=f"{date.strftime('%Y%m%d')}_bse_results.txt",
            print_=True,
            filter_bands=False,
        )
    # # print(df.head())
