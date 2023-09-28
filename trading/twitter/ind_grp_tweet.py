from ..common.config import *
from ..twitter.twitter_util import *
from ..msi.ind_grp import *
from glob import glob
import os
import sys

if __name__ == "__main__":
    os.chdir(msi_ind_grp / "img")
    if check_file(msi_ind_grp_img):
        print(f"Fig {msi_ind_grp_img} found")
    else:
        print("Trying to fetch Ind Grp files")
        x = get_ind_group_image()
        if x:
            print(f"Fetched {msi_ind_grp_img} successfully")
        else:
            print(f"Unable to fetch {msi_ind_grp_img}. Exiting!")
            sys.exit()

    tweet_str = f"{today_dash} [ Top 5% Industry Groups - IND ]"
    try:
        twitter = Twitter()
        twitter.tweet(message=tweet_str, image_path=msi_ind_grp_img)
    except Exception as e:
        print(e)
        print("Could not send tweet!")
