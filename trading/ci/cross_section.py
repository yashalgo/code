# SCREENER TO GET CHARTINK LIQUID UNIVERSE

import os
from ..common.config import *
from ..common.tv_utils import *
from ..common.io import *
from ..ci.ci_utils import *

Condition = """( {cash} ( latest "sma(  volume , 50 ) *  close / 10000000" >= 5 ) ) """
data = GetDataFromChartink(Condition)

# print(data)
s = set(data["nsecode"])
set_to_tv_ind(s, nse_liquid_wl, print_=True, filter_bands=True)
