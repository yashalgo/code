from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import os
from glob import glob
import ntpath
import pandas as pd
import requests
from io import StringIO
import time
import ast


def request_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response


def response_to_df(response):
    data = StringIO(response.text)
    df = pd.read_csv(data)
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


def txt_to_set(fname):
    with open(fname, "r") as f:
        set_1 = ast.literal_eval(f.read())
    return set_1


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


def get_tv_ticker(ticker, filter_bands=True):
    df_bse = get_bse_master()
    nse_filtered_set = get_nse_set(filter_bands=filter_bands)
    error = None
    sec_id = None
    if str(ticker).isdigit():
        try:
            col_name = df_bse.columns[0]
            row = df_bse[df_bse[col_name] == int(ticker)]
            sec_id = row.iloc[0]["Security Id"]
        except:
            # print(f"{i} not found in bse_master_csv. Trying to fetch from url")
            try:
                sec_id = "BSE:" + get_bse_securityId(ticker)
            except:
                error = f"ERROR- Sec_ID not found online: {ticker}"
    else:
        if ticker.replace("NSE:", "") in nse_filtered_set:
            ticker = ticker.replace("&", "_").replace("-", "_")
            nse_ticker = ticker if "NSE" in ticker else "NSE:" + ticker
            sec_id = nse_ticker
        else:
            error = f"ERROR: not in NSE SET: {ticker} "
    return sec_id, error


def tv_str_to_txt(tv_string, outfile):
    # Ensure the directory exists; if not, create it
    directory = os.path.dirname(outfile)
    if directory != "" and not os.path.exists(directory):
        os.makedirs(directory)

    # Write the string to the file
    with open(outfile, "w") as text_file:
        text_file.write(tv_string)
    return


def set_to_tv_ind(s, outfile, print_=True, filter_bands=True):
    print("=============")
    print(f"{outfile}: ")
    temp_set = set()
    for i in s:
        tv_ticker, error = get_tv_ticker(i, filter_bands=filter_bands)
        if error:
            print(error)
        else:
            temp_set.add(tv_ticker)
    tv_string = ",".join(list(temp_set))
    print(f"{len(s)} => {len(temp_set)}")
    if print_ and len(temp_set) != 0:
        tv_str_to_txt(tv_string, outfile)
    print("=============")
    return tv_string


def get_chromedriver_basic(debug=False):
    chrome_options = Options()
    if debug == False:
        chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def change_dir(dst_path):
    if not os.path.isdir(dst_path):
        os.mkdir(dst_path)
    os.chdir(dst_path)
    return


def check_file(fname, path_=None):
    if path_ and os.path.isdir(path_):
        os.chdir(path_)
    files = glob("*.*")
    # print(files)
    basename = ntpath.basename(fname)
    # print(basename)
    if basename in files:
        return True
    else:
        return False


def get_screener_wl(dst_dir, base_url=liquid_stocks_url):
    change_dir(dst_dir)

    if check_file(liquid_stocks_f_txt):
        print(f"{liquid_stocks_txt} already present")
        return

    driver = get_chromedriver_basic()
    stock_links = []
    previous_links = None  # A list to hold links from the previous page for comparison

    page_num = 1

    while True:
        # Navigate to the current page
        driver.get(f"{base_url}?page={page_num}")
        print(f"Page {page_num}")

        # Wait for up to 10 seconds until at least one stock link is found
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//td[@class='text']/a[@target='_blank']")
                )
            )
        except TimeoutException:
            print("No stock links found after waiting for 10 seconds.")
            break

        # Extract stock links from the current page
        current_links = driver.find_elements(
            By.XPATH, "//td[@class='text']/a[@target='_blank']"
        )
        current_links_hrefs = [link.get_attribute("href") for link in current_links]

        # If the links from the current page are the same as the previous page, break out of the loop
        if previous_links == current_links_hrefs:
            print("Reached the last page. Exiting loop.")
            break

        stock_links.extend(current_links_hrefs)
        previous_links = (
            current_links_hrefs.copy()
        )  # Store the current links for the next iteration's comparison

        # Increment page number to navigate to the next page
        page_num += 1
        sleep(2)

    company_names = set(
        [url.split("/company/")[1].split("/")[0] for url in stock_links]
    )
    set_to_tv_ind(company_names, liquid_stocks_txt, print_=True, filter_bands=False)
    set_to_tv_ind(company_names, liquid_stocks_f_txt, print_=True, filter_bands=True)

    # int_company_names = [name for name in company_names if name.isdigit()]
    # set_to_tv_ind(int_company_names, "temp_bse.txt", print_=True, filter_bands=True)

    # print(int_company_names)
    # print(f"Stocks: {len(int_company_names)}")
    # print(f"Stocks: {len(company_names)}")
    driver.close()
