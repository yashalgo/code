from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
from ..common.config import *
from ..common.io import *
from ..common.tv_utils import *
from ..common.chrome_utils import *
from ..exch.exch_utils import *
from ..msi.msi_util import *
import os
import sys


if __name__ == "__main__":
    # check if WL already present
    tv_file = f"{today_blank}_RS.txt"
    change_dir(today_wl)
    if check_file(tv_file):
        print(f"{tv_file} already present. Exiting!")
        sys.exit()

    # check if df already present
    os.chdir(msi_data)
    df_outfile = f"{today_blank}_RS.csv"
    if check_file(df_outfile):
        print(f"{df_outfile} already present.")
        df = pd.read_csv(df_outfile)

    # df not present, fetch df from MSI website
    else:
        driver = get_msi_home(today_wl)

        ## LOGIN COMPLETE
        ##########################

        # SCREENER
        driver.get(msi_screener_url)

        # table view
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for='tableRadio']"))
        )
        label = driver.find_element(By.XPATH, "//label[@for='tableRadio']")
        label.click()

        # find table
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "idealistStocksTable"))
        )
        table = driver.find_element(By.ID, "idealistStocksTable")
        table_html = driver.find_element(By.ID, "idealistStocksTable").get_attribute(
            "outerHTML"
        )

        df = pd.read_html(table_html)[0]

        links = table.find_elements(
            By.XPATH,
            "//a[starts-with(@href, '/mstool/eval/list/') and substring(@href, string-length(@href) - string-length('/evaluation.jsp') +1) = '/evaluation.jsp']",
        )

        tickers = [link.get_attribute("href").split("/")[-2] for link in links]
        tickers = remove_duplicates(tickers)

        df["Ticker"] = tickers
        df.drop(columns=["Price Change", "Price % Change", "Action"], inplace=True)
        df.to_csv(df_outfile)
        print(f"{df_outfile} Saved!")

    os.chdir(today_wl)
    s = set(df["Ticker"])
    # print(s)
    set_to_tv_ind(s, tv_file)
