from ..common.config import *
from ..twitter.twitter_util import *
from ..tji.tji_mm import *
from glob import glob
import os

if __name__ == "__main__":
    plt_outfile = f"{today_blank}_mm.png"
    os.chdir(tji_figs)
    files = glob("*")
    if check_file(plt_outfile):
        print(f"Fig {plt_outfile} found")
    else:
        print("Trying to fetch TJI files")
        x = get_tji_files()
        if x:
            print(f"Fetched {plt_outfile} successfully")
        else:
            print(f"Unable to fetch {plt_outfile}. Exiting!")
            sys.exit()

    tweet_str = f"{today_dash} [ Market Monitor - IND ]"
    try:
        twitter = Twitter()
        twitter.tweet(message=tweet_str, image_path=plt_outfile)
    except Exception as e:
        print(e)
        print("Could not send tweet!")
