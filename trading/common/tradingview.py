import pandas as pd


def set_to_tv(s, outfile):
    s = {x.replace("&", "_").replace("-", "_") for x in s}
    tv_string = ",".join(list(s))
    with open(outfile, "w") as text_file:
        text_file.write(tv_string)
    print(outfile)


def set_to_tv_exchange(s, outfile, exchange="NSE"):
    s = {exchange + ":" + x.replace("&", "_").replace("-", "_") for x in s}
    tv_string = ",".join(list(s))
    with open(outfile, "w") as text_file:
        text_file.write(tv_string)
    print(outfile)


def to_tv(infile):
    df = pd.read_csv(infile)
    df["tv_ticker"] = df["Security Name"].apply(
        lambda x: "NSE:" + x.replace("&", "_").replace("-", "_")
    )
    tv_string = ",".join(list(df["tv_ticker"]))
    outfile = infile.replace(".csv", "_tv.txt")
    with open(outfile, "w") as text_file:
        text_file.write(tv_string)
    print(outfile)


def tv_str_to_list(s):
    x = s.replace("NSE:", "").split(",")
    x.remove("Symbol")
    return x
