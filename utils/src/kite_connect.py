# %%
from kiteconnect import KiteConnect, KiteTicker, exceptions
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import json
import time
import pyotp


def instrument_token(data, symbol):
    """
    This function will return the token number of the instrument from data
    """
    return data[data.tradingsymbol == symbol].instrument_token.values[0]


def login_in_zerodha(api_key, api_secret, user_id, user_pwd, totp_key):
    driver = uc.Chrome()
    driver.get(f"https://kite.trade/connect/login?api_key={api_key}&v=3")
    login_id = WebDriverWait(driver, 10).until(
        lambda x: x.find_element("xpath", '//*[@id="userid"]')
    )
    login_id.send_keys(user_id)

    pwd = WebDriverWait(driver, 10).until(
        lambda x: x.find_element("xpath", '//*[@id="password"]')
    )
    pwd.send_keys(user_pwd)

    submit = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(
            "xpath", '//*[@id="container"]/div/div/div[2]/form/div[4]/button'
        )
    )
    submit.click()

    time.sleep(1)
    # adjustment to code to include totp
    totp = WebDriverWait(driver, 10).until(
        lambda x: x.find_element("xpath", '//*[@label="External TOTP"]')
    )
    print(totp)
    authkey = pyotp.TOTP(totp_key)
    print(authkey.now())
    totp.send_keys(authkey.now())
    # adjustment complete

    continue_btn = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(
            "xpath", '//*[@id="container"]/div/div/div[2]/form/div[3]/button'
        )
    )
    continue_btn.click()

    time.sleep(5)

    url = driver.current_url
    initial_token = url.split("request_token=")[1]
    request_token = initial_token.split("&")[0]

    driver.close()

    kite = KiteConnect(api_key=api_key)
    # print(request_token)
    data = kite.generate_session(request_token, api_secret=api_secret)
    kite.set_access_token(data["access_token"])

    return kite


def get_connection_info(file):
    try:
        with open("connection_info.json") as json_file:
            data = json.load(json_file)
    except:
        print("Error in loading data")
        return
        # Print the type of data variable
    #         print("Type:", type(data))
    return data
