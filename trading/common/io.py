### I/O FUNCTIONS

from glob import glob
from ..common.config import *
import yfinance as yf
import json
import ntpath
import os
import ast


def rename_downloaded_file(dst_dir, new_name):
    # Get a list of all files in the directory sorted by modification time
    list_of_files = sorted(
        (os.path.join(dst_dir, base) for base in os.listdir(dst_dir)),
        key=os.path.getmtime,
    )

    # Get the most recently modified file
    latest_file = list_of_files[-1]

    # Rename the file
    os.rename(latest_file, os.path.join(dst_dir, new_name))


def txt_to_str(fname):
    with open(fname, "r") as file:
        data = file.read().replace("\n", "")
    return data


def txt_to_set(fname):
    with open(fname, "r") as f:
        set_1 = ast.literal_eval(f.read())
    return set_1


def get_yf_df(symbol, period_="1mo"):
    df2 = yf.download(symbol, period=period_, progress=False)
    df2.rename(columns=str.lower, inplace=True)
    df2.drop("close", axis=1, inplace=True)
    df2.rename(columns={"adj close": "close"}, inplace=True)
    df2.reset_index(inplace=True)
    return df2


def remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def convert_yf_df(df2):
    df2.rename(columns=str.lower, inplace=True)
    df2.drop("close", axis=1, inplace=True)
    df2.rename(columns={"adj close": "close"}, inplace=True)
    df2.reset_index(inplace=True)
    return df2


def read_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data


def get_latest_file(path=downloads):
    path_ = os.getcwd()
    os.chdir(path)
    list_of_files = glob("*")  # * means all files and subdirectories
    latest_file = max(list_of_files, key=os.path.getctime)
    file_name = os.path.basename(latest_file)
    os.chdir(path_)
    return file_name


def check_file(fname, path_=None):
    if path_ and os.path.isdir(path_):
        os.chdir(path_)
    files = glob("*.*")
    # print(files)
    basename = ntpath.basename(fname)
    # print(basename)
    if basename in files:
        return True
    else:
        return False


def delete_files_with_string_recursive(target_string, folder_path=exchange_data):
    deleted_files_count = 0

    # Walk through folder and sub-folders
    for dirpath, dirnames, filenames in os.walk(folder_path):
        # Filter files that contain the target string and do not contain today's date
        files_to_delete = [
            f for f in filenames if target_string in f and today_blank not in f
        ]

        for file in files_to_delete:
            os.remove(os.path.join(dirpath, file))
            deleted_files_count += 1

    print(f"Deleted {deleted_files_count} files.")


def change_dir(dst_path):
    if not os.path.isdir(dst_path):
        os.mkdir(dst_path)
    os.chdir(dst_path)
    return


def india_int_format(n):
    s = str(n)[::-1]
    groups = [s[i : i + 2] for i in range(0, len(s), 2)]
    return ",".join(groups)[::-1]
