### TV FUNCTIONS

import pandas as pd
from .config import *
from ..exch.exch_utils import *
import os


def get_tv_ticker(ticker, filter_bands=True):
    df_bse = get_bse_master()
    nse_filtered_set = get_nse_set(filter_bands=filter_bands)
    error = None
    sec_id = None
    if str(ticker).isdigit():
        try:
            col_name = df_bse.columns[0]
            row = df_bse[df_bse[col_name] == int(ticker)]
            sec_id = row.iloc[0]["Security Id"]
        except:
            # print(f"{i} not found in bse_master_csv. Trying to fetch from url")
            try:
                sec_id = "BSE:" + get_bse_securityId(ticker)
            except:
                error = f"ERROR- Sec_ID not found online: {ticker}"
    else:
        if ticker.replace("NSE:", "") in nse_filtered_set:
            ticker = ticker.replace("&", "_").replace("-", "_")
            nse_ticker = ticker if "NSE" in ticker else "NSE:" + ticker
            sec_id = nse_ticker
        else:
            error = f"ERROR: not in NSE SET: {ticker} "
    return sec_id, error


def set_to_tv_ind(s, outfile, print_=True, filter_bands=True):
    print("=============")
    print(f"{outfile}: ")
    temp_set = set()
    for i in s:
        tv_ticker, error = get_tv_ticker(i, filter_bands=filter_bands)
        if error:
            print(error)
        else:
            temp_set.add(tv_ticker)
    tv_string = ",".join(list(temp_set))
    print(f"{len(s)} => {len(temp_set)}")
    if print_ and len(temp_set) != 0:
        tv_str_to_txt(tv_string, outfile)
    print("=============")
    return tv_string


def set_to_tv_us(s, outfile, print_=True):
    tv_string = ",".join([i.replace("&", "_").replace("-", "_") for i in s])
    if print_:
        tv_str_to_txt(tv_string, outfile)
    return tv_string


def tv_str_to_txt(tv_string, outfile):
    # Ensure the directory exists; if not, create it
    directory = os.path.dirname(outfile)
    if directory != "" and not os.path.exists(directory):
        os.makedirs(directory)

    # Write the string to the file
    with open(outfile, "w") as text_file:
        text_file.write(tv_string)
    return


if __name__ == "__main__":
    t = get_tv_ticker("500006")
    print(t)

# def get_custom_index(df):
