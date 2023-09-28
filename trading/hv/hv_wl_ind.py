from ..common.config import *
from ..common.io import *
from ..ci.ci_utils import *

if __name__ == "__main__":
    # HVQ
    hv_outfile = f"{today_blank}_HV.txt"
    get_ci_wl(hv, hv_outfile, today_wl)

    # time.sleep(5)
    # hvy_outfile = f"{today_blank}_HVY.txt"
    # get_ci_wl(hvy, hvy_outfile, today_wl)
