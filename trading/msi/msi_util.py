import time
import os
import re
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..common.tv_utils import *

from ..common.chrome_utils import *
from ..common.config import *
from ..common.io import *


def parse_market_cap(value):
    value = value.replace(",", "")

    if "L" in value:
        return float(value.replace(" L", "")) * 0.01
    elif "Cr" in value:
        return float(value.replace(" Cr", ""))
    else:
        return float(value)


def apply_get_tv_ticker(ticker):
    sec_id, error = get_tv_ticker(ticker)
    return sec_id if error is None else None


def wait_for_download(directory, timeout=60):
    seconds = 0
    while seconds < timeout:
        time.sleep(1)
        downloaded_files = os.listdir(directory)
        if any([filename.endswith(".crdownload") for filename in downloaded_files]):
            seconds += 1
        else:
            return True
    raise Exception("Download did not complete in the allotted time")


def custom_rank(series, tie_breaker_series, ascending=True):
    # Convert series to negative for descending ranking
    multiplier = 1 if ascending else -1
    series = multiplier * series
    tie_breaker_series = multiplier * tie_breaker_series

    # Use argsort twice to get the ranking
    return np.argsort(np.argsort(series + tie_breaker_series * 1e-10))


def format_value(val):
    if isinstance(val, float) and val.is_integer():
        return int(val)
    return val


def get_numerical_value(string):
    value = re.sub(r"\D", "", string)
    if value.isdigit():
        return int(value)
    else:
        return None


def get_msi_home(download_path):
    driver = get_chromedriver2(download_path)
    driver.get(SIGN_IN_URL)

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept']"))
        ).click()
    except:
        pass

    credentials = read_json(cred_msi)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "landingIframe"))
    )
    iframe = driver.find_element(By.ID, "landingIframe")
    driver.switch_to.frame(iframe)

    username_field = driver.find_element(By.ID, "loginEmail")
    username_field.send_keys(credentials["email_id"])
    password_field = driver.find_element(By.ID, "loginPassword")
    password_field.send_keys(credentials["password"])
    submit_button = driver.find_element(By.XPATH, "//a[normalize-space()='Sign In']")
    submit_button.click()

    WebDriverWait(driver, 20).until(EC.url_to_be(LANDING_URL))
    return driver
