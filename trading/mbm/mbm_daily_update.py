# CODE TO GET ALL STOCKS FROM A CHARTINK DASHBOARD

from ..common.chrome_utils import *
from ..common.config import *
from ..common.io import *
from ..ci.db import *

import pandas as pd
import os
import subprocess

DOWLOAD_FILE = "MBM.csv"
OUTFILE = f"{today_blank}_mbm.csv"
DASHBOARD_URL = "https://chartink.com/dashboard/196038"
PATH = mbm_db


def get_latest_mbm():
    if check_file(OUTFILE, PATH):
        print(f"File {OUTFILE} already present")
        os.chdir(PATH)
        df = pd.read_csv(OUTFILE)
        df["date"] = df.apply(
            lambda row: correct_year(
                f"{row['date'].split(' ')[0]} {row['date'].split(' ')[1]}",
                datetime.now().year,
            ),
            axis=1,
        )

        return df
    else:
        try:
            if get_ci_db(DOWLOAD_FILE, DASHBOARD_URL, PATH):
                os.rename(DOWLOAD_FILE, OUTFILE)
                return get_latest_mbm()
        except Exception as e:
            print(f"Error fetching file {DOWLOAD_FILE}: {e}")
            return None


def correct_year(date_str, year):
    try:
        day_str = "".join(filter(str.isdigit, date_str.split(" ")[0]))
        month_str = date_str.split(" ")[1]
        date_obj = datetime.strptime(f"{day_str} {month_str} {year}", "%d %b %Y")
        return date_obj.strftime("%Y%m%d") + "T"
    except Exception as e:
        return None


def update_mbm_files():
    try:
        latest_mbm_df = get_latest_mbm()
    except:
        print("Could not fetch MBM file")
        return False

    todayT = today_blank + "T"

    print(latest_mbm_df.head())
    for column in latest_mbm_df.columns:
        if column != "date":  # Skip the date column
            # Read the existing individual file
            fname = f"{column.upper()}.csv"
            file_path = os.path.join(nse_breadth_data, fname)
            print(fname, end=" | ")
            if os.path.exists(file_path):
                print(f"File found", end=" | ")
                individual_df = pd.read_csv(file_path, header=None)
                last_date = individual_df.iloc[-1, 0]
                if last_date == todayT:
                    print(f"File already up to date")
                    continue  # Skip the rest of the loop for this file
            else:
                print(f"{fname} not found", end=" | ")
                individual_df = pd.DataFrame()
            print("Updating")
            new_data = pd.DataFrame()
            new_data[0] = latest_mbm_df["date"]
            for i in range(1, 5):
                new_data[i] = latest_mbm_df[column]
            new_data[5] = 0  # Last column with all zeros

            updated_df = pd.concat([individual_df, new_data])
            updated_df = updated_df.drop_duplicates(
                subset=[0], keep="last"
            )  # Remove duplicates based on date
            updated_df = updated_df.sort_values(by=[0])  # Sort by date

            # Save the updated DataFrame back to the individual file
            updated_df.to_csv(file_path, index=False, header=False)
    return True


def git_operations():
    # Run git status and capture the output
    result = subprocess.run(["git", "status"], capture_output=True, text=True)

    # Check if the output indicates that there are no changes to commit
    if "nothing to commit, working tree clean" in result.stdout:
        print("No changes to commit.")
    else:
        # Run the git commands since there are changes
        print("Pushing changes")

        subprocess.run(
            ["cd", "/Users/yash/Desktop/Trading/code/seed_yashalgo_nse_breadth"]
        )
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "Update data"])
        subprocess.run(["git", "push"])


if __name__ == "__main__":
    if update_mbm_files():
        # Changed this line to run the new function for git operations
        git_operations()
