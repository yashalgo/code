# SCREENER TO GET CHARTINK LIQUID UNIVERSE

import os
from ..common.config import *
from ..common.tv_utils import *
from ..common.io import *
from ..ci.ci_utils import *

Condition = """( {cash} ( latest close >= weekly max( 52 , weekly high ) * 0.75 and latest close >= weekly min( 52 , weekly low ) * 1.3 and latest {custom_indicator_65569_start}"sma(  volume , 50 ) *  close / 10000000"{custom_indicator_65569_end} >= 5 ) ) """
data = GetDataFromChartink(Condition)

# print(data)
s = set(data["nsecode"])
os.chdir(today_wl)
set_to_tv_ind(s, f"{today_blank}_mom_ind.txt", print_=True, filter_bands=True)
