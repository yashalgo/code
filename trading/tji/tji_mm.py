from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from ..common.config import *
from ..common.chrome_utils import *
from ..common.io import *
import time
import sys


def get_tji_files():
    os.chdir(tji_mm)
    mm_fname = f"{today_blank}_mm.csv"
    plt_outfile = f"{today_blank}_mm.png"

    if check_file(mm_fname):
        print(f"{mm_fname} already present. Exiting")
        return

    # SIGN IN
    driver = get_chromedriver_basic()
    driver.get(tijori_signin_url)

    credentials = read_json(cred_tji)

    driver.find_element(By.ID, "email").send_keys(credentials["email_id"])
    driver.find_element(By.ID, "pwd-field").send_keys(credentials["password"])

    login_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign in']"))
    )
    login_button.click()
    time.sleep(5)
    print("Switching to MM")
    driver.get(tijori_mm_url)
    time.sleep(5)

    table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "market__table__niche"))
    )
    df = pd.read_html(driver.execute_script("return arguments[0].outerHTML;", table))[0]
    driver.quit()

    ###### df processing
    df_cleaned = df.drop(columns=["WEIGHT", "1D", "2YR*", "3YR*", "5YR*"])
    df_cleaned.rename(columns={"Unnamed: 0": "Niche"}, inplace=True)
    df_cleaned["Niche"] = df_cleaned["Niche"].str.replace("TJI ", "")

    numeric_columns = df_cleaned.select_dtypes(include=["object"]).columns.drop("Niche")
    for column in numeric_columns:
        df_cleaned[column] = df_cleaned[column].str.rstrip("%").astype("float")

    df_cleaned["Rank 1W"] = df_cleaned["1W"].rank(ascending=False)
    df_cleaned["Rank 1M"] = df_cleaned["1M"].rank(ascending=False)
    df_cleaned["Rank 3M"] = df_cleaned["3M"].rank(ascending=False)
    df_cleaned["Rank 6M"] = df_cleaned["6M"].rank(ascending=False)
    df_cleaned["Rank 1YR*"] = df_cleaned["1YR*"].rank(ascending=False)

    df_cleaned.to_csv(mm_fname)
    rank_filter = 5
    df_top = df_cleaned[
        (
            df_cleaned[["Rank 1W", "Rank 1M", "Rank 3M", "Rank 6M", "Rank 1YR*"]]
            <= rank_filter
        ).any(axis=1)
    ]

    df_ranks = df_top[
        ["Niche", "Rank 1W", "Rank 1M", "Rank 3M", "Rank 6M", "Rank 1YR*"]
    ].set_index("Niche")

    os.chdir(tji_figs)

    fig, ax = plt.subplots(figsize=(10, 16))  # Create a subplot to get the Axes object
    sns.heatmap(df_ranks, cmap="summer", linewidths=0.5, annot=True, cbar=False)
    ax.xaxis.tick_top()  # Move x-axis labels to top

    ###
    plt.tight_layout()  # Add this line before saving the figure
    plt.savefig(plt_outfile)
    return True


if __name__ == "__main__":
    get_tji_files()
    # x = get_chromedriver_basic()
    # print(x)
    # y = get_chromedriver()
    # print(y)
