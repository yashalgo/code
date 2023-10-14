### WEB INTERACTION COMMON FUNCTIONS

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ..common.config import *
import requests
import pandas as pd
from io import StringIO
import os


def request_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response


def get_chromedriver2(download_dir, headless=True):
    download_dir = os.path.abspath(download_dir)
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    chrome_options = webdriver.ChromeOptions()

    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")

    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
        },
    )

    driver = webdriver.Chrome(options=chrome_options)
    return driver


# OLD
# def get_chromedriver2(download_dir, headless=True):
#     download_dir = os.path.abspath(download_dir)
#     print(download_dir)
#     if not os.path.exists(download_dir):
#         os.makedirs(download_dir)

#     chrome_options = webdriver.ChromeOptions()

#     if headless:
#         chrome_options.add_argument("--headless")
#         chrome_options.add_argument(
#             "--window-size=1920x1080"
#         )  # Set a default window size (optional)

#     chrome_options.add_experimental_option(
#         "prefs",
#         {
#             "download.default_directory": download_dir,
#             "download.prompt_for_download": False,
#             "download.directory_upgrade": True,
#             "plugins.always_open_pdf_externally": True,
#         },
#     )

#     driver = webdriver.Chrome(options=chrome_options)
#     return driver


def get_chromedriver(
    debug=False, download_path=today_wl, driver_path=chromedriver_path
):
    chrome_options = Options()
    prefs = {"download.default_directory": str(download_path)}
    chrome_options.add_experimental_option("prefs", prefs)
    if not debug:
        chrome_options.add_argument("--headless")
    print(webdriver.__version__)
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    return driver


def get_chromedriver_basic(debug=False):
    chrome_options = Options()
    if debug == False:
        chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def response_to_df(response):
    data = StringIO(response.text)
    df = pd.read_csv(data)
    return df
