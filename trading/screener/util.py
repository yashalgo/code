from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
from ..common.chrome_utils import *
from ..common.tv_utils import *
from ..common.config import *


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
