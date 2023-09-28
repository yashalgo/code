import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

warnings.simplefilter(action="ignore", category=pd.errors.SettingWithCopyWarning)

from ..common.chrome_utils import *
from ..common.config import *
from ..common.io import *
from ..msi.msi_util import *


def get_msi_data():
    outfile = os.path.join(msi_raw_data, f"{today_blank}_msi_raw.csv")
    if os.path.exists(outfile):
        print(f"File already exists: {outfile}")
        return pd.read_csv(outfile)

    driver = get_msi_home(msi_raw_data)
    driver.get(MSI_SCREENER)

    # CANCEL FILTER BUTTON
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[text()='Cancel' and @onclick='javascript: confirmBox.no();']",
                )
            )
        ).click()
    except:
        pass

    # EXPORT DATA BUTTON
    try:
        WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.ID, "ideaDownloadList"))
        ).click()
        wait_for_download(msi_ind_grp)
    except:
        pass

    original_filename = os.path.join(msi_raw_data, "Filter_India_Stocks.csv")
    os.rename(original_filename, outfile)
    print(os.getcwd())
    df = pd.read_csv(outfile)
    driver.quit()
    return df


if __name__ == "__main__":
    get_msi_data()
