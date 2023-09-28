### CHARTINK UTILITY FUNCTIONS

from ..common.config import *
from ..common.tv_utils import *
from ..common.io import *
from ..common.chrome_utils import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import shutil


def get_ci_wl(chartink_url, outfile="temp.txt", dst_path=today_wl):
    xl_file = outfile.replace("txt", "xlsx")

    change_dir(dst_path)
    if check_file(outfile):
        print(f"{outfile} already present")
        return
    elif check_file(xl_file):
        print(f"{xl_file} already present")
        df = pd.read_excel(xl_file)
    else:
        driver = get_chromedriver2(today_wl)
        driver.get(chartink_url)
        time.sleep(10)

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Excel']")
            )
        ).click()
        time.sleep(5)
        # print("in dst_path")

        file = glob("*.xlsx")[0]
        df = pd.read_excel(file)
        shutil.move(file, xl_file)

        print(f"Successfully downloaded {xl_file} to {dst_path}")
    os.getcwd()
    os.chdir(dst_path)
    ci_to_tv(df, outfile)
    os.remove(xl_file)
    print("------------------------")
    print(f"Removing {xl_file}")
    return


def ci_to_tv(df, outfile):
    tickers = set(df["Unnamed: 2"])
    # print(f"Tickers: {len(tickers)}")
    set_to_tv_ind(tickers, outfile)
    return


def GetDataFromChartink(payload):
    ci_screener_link = "https://chartink.com/screener/"
    ci_screener_url = "https://chartink.com/screener/process"
    payload = {"scan_clause": payload}

    with requests.Session() as s:
        r = s.get(ci_screener_link)
        soup = BeautifulSoup(r.text, "html.parser")
        csrf = soup.select_one("[name='csrf-token']")["content"]
        s.headers["x-csrf-token"] = csrf
        r = s.post(ci_screener_url, data=payload)
        df = pd.DataFrame(r.json()["data"])
    return df


if __name__ == "__main__":
    print("Hi!")
