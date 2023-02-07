#!/usr/bin/python3
# coding: utf-8

from libs import *
from helper_functions import *
from paths import *

fcustom = Custom()


# ------FILTERS------


today = datetime.today().strftime('%Y%m%d')

today_ = datetime.today().strftime('%Y/%m/%d')

path_ = q_wl / today_
if not os.path.isdir(path_):
    os.mkdir(path_)
os.chdir(path_)

outfile_ = today + '_US.txt'
files = glob('**/*_US.txt', recursive = True)
print(files)
if outfile_ in files:
    print('File already present. Aborting!')
    exit()


# In[5]:


limit = 100

#1-month performance
perf1 = 'Month +50%'
vol1 = 'Month - Over 5%'

#3-month performance
perf3 = 'Quarter +50%'
vol3 = 'Month - Over 5%'

#6-month performance
perf6 = 'Half +100%'
vol6 = 'Month - Over 5%'

#Price
price = 'Any'
cols = [0,1,2,3,4,6,43,44,45,51,52,53,63,65,68]

filters_dict1 = {'Market Cap.': '+Micro (over $50mln)','Performance': perf1, 'Price': price,
                'Volatility': vol1, 'Average Volume': 'Over 100K'}

filters_dict3 = filters_dict1.copy()
filters_dict3['Performance'] = perf3
filters_dict3['Volatility'] = vol3

filters_dict6 = filters_dict1.copy()
filters_dict6['Performance'] = perf6
filters_dict6['Volatility'] = vol6

# --------------1 MONTH GAINERS-------------

fcustom.set_filter(filters_dict=filters_dict1)
df1 = fcustom.screener_view(columns=cols, sleep_sec = 1, order= 'Performance (Month)', ascend=False)
print(df1.shape[0])
df1 = df1.head(limit)

df1.shape[0]


# --------------3 MONTH GAINERS-------------

fcustom.set_filter(filters_dict=filters_dict3)
df3 = fcustom.screener_view(columns=cols, sleep_sec = 1,  order='Performance (Quarter)', ascend=False)
print(df3.shape[0])
df3 = df3.head(limit)

df3.shape[0]


# --------------6 MONTH GAINERS-------------
fcustom.set_filter(filters_dict=filters_dict6)
df6 = fcustom.screener_view(columns=cols, sleep_sec = 1,  order='Performance (Half Year)', ascend=False)
print(df6.shape[0])

df6 = df6.head(limit)

df6.shape[0]


# --------------MERGE-------------
df_final = pd.concat([df1, df3, df6], axis=0)
df_final = df_final.drop_duplicates(subset=['Ticker'], keep='first')


df_final.shape[0]

s = set(df_final['Ticker'])

set_to_tv_US(s)

