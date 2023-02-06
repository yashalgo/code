# %%
from datetime import date, datetime, timedelta
import pandas as pd
import os
from helper_functions import *

# %%
today = datetime.datetime.today().strftime('%Y/%m/%d')

# %%
os.chdir('/Users/yash/Desktop/Trading/VCP/watchlists/'+today)

# %%
df = pd.read_excel('VCP.xlsx')

# %%
today_ = datetime.datetime.today().strftime('%Y%m%d')

# %%
s = set()

print(df['Unnamed: 2'].shape)
s.update(set(df['Unnamed: 2']))
# print(len(s))
set_to_tv(s, today_ + '_VCP.txt')

#TEST
