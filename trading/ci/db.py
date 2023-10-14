# CODE TO GET ALL STOCKS FROM A CHARTINK DASHBOARD

from selenium import webdriver
from ..common.chrome_utils import *
from ..common.io import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_ci_db(
    OUTFILE="Top Gainers.csv",
    DASHBOARD_URL="https://chartink.com/dashboard/158123?open-widget=1940413",
    path_=today_wl,
):
    if check_file(OUTFILE, path_):
        print(f"File {OUTFILE} already present")
        return True

    driver = get_chromedriver2(path_)

    # Load the local HTML page
    driver.get(DASHBOARD_URL)
    xpath = '//div[@title="Download results"]'

    try:
        # Find the element containing the download button
        download_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

        time.sleep(10)
        driver.execute_script("arguments[0].style.display = 'block';", download_div)

        # Use JavaScript to click the download button
        download_button = driver.find_element(By.XPATH, xpath + "/a")
        driver.execute_script("arguments[0].click();", download_button)

        print(f"Fetch {OUTFILE} Successful!")
        time.sleep(1)
        driver.quit()
        return True
    except Exception as e:
        print("Error:", e)
        return False
