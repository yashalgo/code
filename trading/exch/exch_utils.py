from ..common.config import *
from ..common.io import *
from ..common.chrome_utils import *
import os
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import pandas_market_calendars as mcal


def get_bse_securityId(id):
    url = f"https://m.bseindia.com/StockReach.aspx?scripcd={str(id)}"
    # Start the WebDriver (replace 'path_to_chromedriver' with the actual path)
    driver = get_chromedriver_basic()
    driver.get(url)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "tdCShortName"))
    )
    element = driver.find_element(By.ID, "tdCShortName")
    text = element.text
    # print(text)
    time.sleep(1)
    driver.quit()
    return text


def get_combined_master():
    path_ = os.getcwd()

    nse_df = get_nse_master()
    nse_df.columns = nse_df.columns.str.strip()

    bse_df = get_bse_master()
    # print(bse_df.head())
    # ["A ", "B ", "T ", "X", "XT"]
    bse_df = bse_df[bse_df["Group"].isin(["A ", "B ", "T ", "X", "XT"])]
    bse_df.columns = bse_df.columns.str.strip()
    # print(bse_df.columns)
    # print(nse_df.shape[0], bse_df.shape[0])
    os.chdir(exchange_data)
    if check_file(combined_csv):
        print(f"Latest file {combined_csv} already present")
        merged_df = pd.read_csv(combined_csv, index_col=False)
    else:
        print(f"Fetching file {combined_csv}")
        merged_df = pd.merge(
            nse_df[["SYMBOL", "SERIES", "ISIN NUMBER"]],
            bse_df[["Security Code", "Security Id", "ISIN No", "Group"]].rename(
                columns={
                    "Security Id": "BSE_ID",
                    "Security Code": "BSE_CODE",
                    "Group": "BSE_GROUP",
                }
            ),
            left_on="ISIN NUMBER",
            right_on="ISIN No",
            how="outer",
        )
        merged_df.rename(
            columns={
                "ISIN NUMBER": "NSE_ISIN",
                "SYMBOL": "NSE_SYMBOL",
                "SERIES": "NSE_SERIES",
                "ISIN No": "BSE_ISIN",
            },
            inplace=True,
        )

        reordered_columns = [
            "NSE_ISIN",
            "NSE_SYMBOL",
            "NSE_SERIES",
            "BSE_ISIN",
            "BSE_CODE",
            "BSE_ID",
            "BSE_GROUP",
        ]
        merged_df = merged_df.reindex(columns=reordered_columns)

        # print(merged_df.shape[0])
        merged_df.to_csv(combined_csv, index=False)
    os.chdir(path_)
    return merged_df


def get_bse_master():
    # not working, using list of scrips as of 27072023
    path_ = os.getcwd()
    os.chdir(exchange_data)

    if check_file(bse_master_csv):
        # print(f"Latest file {bse_master_csv} already present")
        df = pd.read_csv(bse_master_csv, index_col=False)
        # print(df.columns)
    else:
        print(f"Fetching file {bse_master_csv}")
        response = request_url(bse_master_url)
        print(response.text)
        df = response_to_df(response)
        df["Security_No"] = df.index
        df.to_csv(bse_master_csv)
    os.chdir(path_)
    return df


def get_csv(url, outfile, path_=exchange_data):
    os.chdir(path_)
    if check_file(outfile):
        print(f"Latest file {outfile} already present")
        df = pd.read_csv(outfile)
    else:
        response = request_url(url)
        df = response_to_df(response)
        df.to_csv(outfile)
    return df


def get_nse_master():
    path_ = os.getcwd()
    df = get_csv(nse_master_url, nse_master_csv, exchange_data)
    os.chdir(path_)
    return df


def get_nse_set(filter_bands=True):
    path_ = os.getcwd()
    os.chdir(exchange_data)
    f = nse_bands_txt_f if filter_bands else nse_bands_txt

    if check_file(f):
        # print(f"Latest file {nse_bands_txt} for {today_blank} already present")
        filtered_set = txt_to_set(f)
    else:
        print(f"Fetching file {f}")
        df = get_csv(nse_bands_url, nse_bands_csv)
        ignore_filters = ["2", "5"]
        if filter_bands:
            filtered_stocks = df.loc[~df["Band"].isin(ignore_filters)]
            filtered_set = set(filtered_stocks["Symbol"])
        else:
            filtered_set = set(df["Symbol"])
        with open(f, "w") as output:
            output.write(str(filtered_set))
    os.chdir(path_)
    # print(type(filtered_set), len(filtered_set))
    return filtered_set


def get_bse_earnings():
    path_ = os.getcwd()
    os.chdir(exchange_data)

    if check_file(bse_results_csv):
        print(f"Latest file {bse_results_csv} already present")
        df = pd.read_csv(bse_results_csv)
    else:
        with open(bse_results_html, "r") as f:
            contents = f.read()
        soup = BeautifulSoup(contents, "html.parser")
        tables = soup.find_all("table")
        table_data = tables[2]
        rows = table_data.find_all("tr")
        data = []
        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])  # Remove empty values
        df = pd.DataFrame(data, columns=["ID", "Name", "Date"])
        df = df.drop(0)
        df = df.reset_index(drop=True)
        df.to_csv(bse_results_csv)
    os.chdir(path_)
    return df


def get_bse_trading_days(range=252):
    end_date = datetime.today()
    start_date = end_date - timedelta(
        days=252 * 2
    )  # Roughly account for weekends and holidays

    bse = mcal.get_calendar("BSE")
    schedule = bse.schedule(start_date=start_date, end_date=end_date)
    trading_days = mcal.date_range(schedule, frequency="1D")
    trading_days = trading_days[-1 * range :]
    return trading_days


# download csv for every value in broad_indices to path exch_data, skip if already present
def get_nse_indices(list_indices=nse_broad_indices):
    path_ = os.getcwd()
    os.chdir(nse_indices)
    for index_url in list_indices:
        index = (
            index_url.split("/")[-1].split("_")[1].replace("list.csv", "")
        )  # change this
        filename = f"{today_blank}_{index}.csv"
        try:
            df = get_csv(index_url, filename, nse_indices)
            # print(df.head())
            print(f"{filename} downloaded successfully!")
        except Exception as e:
            print(f"An error occurred while downloading {filename}: {str(e)}")
    os.chdir(path_)
    return


if __name__ == "__main__":
    # get_bse_earnings()
    # get_bse_csv()
    # id = get_bse_securityId(531562)
    # print(id)
    # s = get_nse_set(filter_bands=False)
    # get_nse_set()
    # get_nse_indices()
    df = get_combined_master()
    # print(df.head())
    pass
