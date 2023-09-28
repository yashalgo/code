from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import pandas as pd
import warnings
import json

warnings.simplefilter(action="ignore", category=pd.errors.SettingWithCopyWarning)

from ..common.chrome_utils import *
from ..common.config import *
from ..common.io import *
from ..common.tv_utils import *
from ..msi.msi_util import *
from ..msi.ind_grp import *


def get_index_str(df):
    df = df.dropna(subset=["SecID"])
    top_10 = df.sort_values(by="MarketCapital", ascending=False).head(10)

    total_market_cap = top_10["MarketCapital"].sum()

    # Calculate weights for each stock
    top_10["Weight"] = top_10["MarketCapital"] / total_market_cap

    # Filter out stocks with weight less than 0.05
    filtered_top_10 = top_10[top_10["Weight"] >= 0.05]

    weighted_string = "+".join(
        [f"{row['SecID']}*{row['Weight']:.2f}" for _, row in filtered_top_10.iterrows()]
    )

    print(weighted_string)
    return weighted_string


def get_ind_wl(driver, grp_id, dst_dir):
    os.chdir(dst_dir)
    outfile = f"{grp_id}_{today_blank}.csv"
    if check_file(outfile):
        print(f"File already exists: {outfile}")
        return pd.read_csv(outfile, index_col=False)
    else:
        print(f"Fetching {outfile}")

    ind_grp_url = (
        f"https://marketsmithindia.com/mstool/eval/list/{grp_id}/evaluation.jsp#/"
    )
    driver.get(ind_grp_url)
    try:
        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "industryExport"))
        ).click()
        wait_for_download(dst_dir)
        rename_downloaded_file(dst_dir, outfile)
        time.sleep(2)

        df = pd.read_csv(outfile, index_col=False)
        # print(df.head())
        df["SecID"] = df["Symbol"].apply(apply_get_tv_ticker)
        df["MarketCapital"] = df["MarketCapital"].apply(parse_market_cap)
        df.to_csv(outfile)

        print(f"Successful: {outfile}")
        return df
    except Exception as e:
        print(f"Error fetching {outfile}: {e}")
        pass


if __name__ == "__main__":
    os.chdir(msi_ind_grp / "csv")
    if not check_file(msi_ind_grp_csv_f):
        print(f"Fetching master Ind Grp file: {msi_ind_grp_csv_f}")
        get_ind_group_image()
    else:
        print(f"File already present: {msi_ind_grp_csv_f}")

    df_master = pd.read_csv(msi_ind_grp_csv_f, index_col=False)

    driver = get_msi_home(msi_ind_grp_wl)

    # custon indices

    # Load the JSON file (if it exists) or initialize an empty dictionary
    os.chdir(msi_ind_grp)
    json_filename = "msi_indices.json"
    if check_file(json_filename):
        with open(json_filename, "r") as f:
            data = json.load(f)
    else:
        data = {}

    for i, row in df_master.iterrows():
        grp_id = row.Symbol
        ind_grp = row["Industry Group"]
        print(grp_id, ind_grp)

        try:
            df = get_ind_wl(driver, grp_id, msi_ind_grp_wl)
        except:
            print(f"Error fetching df for group: {ind_grp}")

        tv_wl = f"{grp_id}_{today_blank}.txt"
        # print(df.head())
        if not check_file(tv_wl):
            os.chdir(msi_ind_grp / "tv")
            # print(df.head())
            set_to_tv_ind(set(df["Symbol"]), tv_wl, True, False)

        if grp_id not in data or data[grp_id]["date_updated"] != today_blank:
            index_str = get_index_str(df)
            data[grp_id] = {"index_str": index_str, "date_updated": today_blank}
    os.chdir(msi_ind_grp)
    with open(json_filename, "w") as f:
        json.dump(data, f, indent=4)
    driver.close()
