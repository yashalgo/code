# Required Libraries
import pandas as pd
from datetime import datetime
import urllib.parse
import os

from ..common.config import *


# Function to convert date to YYYYMMDDT format
def correct_year(date_str, year):
    try:
        day_str = "".join(filter(str.isdigit, date_str.split(" ")[0]))
        month_str = date_str.split(" ")[1]
        date_obj = datetime.strptime(f"{day_str} {month_str} {year}", "%d %b %Y")
        return date_obj.strftime("%Y%m%d") + "T"
    except Exception as e:
        return None


# Function to create CSV files for each column
def create_csv_for_column(column_name, df):
    file_name = column_name.upper() + ".csv"
    file_path = f"{file_name}"
    new_df = pd.DataFrame()
    new_df["date"] = df["date"]
    for i in range(4):
        new_df[str(i + 1)] = df[column_name]
    new_df["last_col"] = 0
    new_df.to_csv(file_path, index=False, header=False)
    return file_path


# Read the MBM.csv file with manually added years
os.chdir(code / "mbm/data")
mbm_df = pd.read_csv("MBM.csv")

# Combine the 'date' and 'Year' columns to form a new 'date' column in YYYYMMDDT format
mbm_df["date"] = mbm_df.apply(
    lambda row: correct_year(
        f"{row['date'].split(' ')[0]} {row['date'].split(' ')[1]}", row["Year"]
    ),
    axis=1,
)

# Drop the 'Year' column as it is no longer needed
mbm_df.drop("Year", axis=1, inplace=True)

# Sort by date in ascending order
mbm_df = mbm_df.sort_values(by="date").reset_index(drop=True)

# Generate the CSV files
generated_files = []
for col in mbm_df.columns:
    if col != "date":
        generated_files.append(create_csv_for_column(col, mbm_df))

print(generated_files)
