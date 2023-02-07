#!/usr/bin/python3
# coding: utf-8

# In[1]:
import sys
import subprocess
import pkg_resources
from finvizfinance.screener.custom import Custom
from datetime import datetime
import pandas as pd
import os
from glob import glob
import sys


# In[2]:


fcustom = Custom()


# ------FILTERS------

# In[3]:


today = datetime.today().strftime('%Y%m%d')


# In[8]:


today_ = datetime.today().strftime('%Y/%m/%d')


# In[9]:


path_ = "/Users/yash/Desktop/Trading/Q/watchlists/"+today_
if not os.path.isdir(path_):
    os.mkdir(path_)
os.chdir(path_)
os.getcwd()


# In[10]:


# In[4]:
outfile_ = today + '_US.txt'
files = glob('**/*_US.txt', recursive = True)
print(files)
if outfile_ in files:
    print('File already present. Aborting!')
    exit()


# In[4]:


def set_to_tv(s, outfile = today + '_US.txt', exchange = 'NASDAQ'):
#     s = {exchange + ":" + x.replace("&","_").replace("-","_") for x in s}
    s = {x.replace("&","_").replace("-","_") for x in s}

    tv_string = ','.join(list(s))
    with open(outfile, "w") as text_file:
        text_file.write(tv_string)
    print(outfile)


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

# In[7]:


fcustom.set_filter(filters_dict=filters_dict1)
df1 = fcustom.screener_view(columns=cols, sleep_sec = 1, order= 'Performance (Month)', ascend=False)
print(df1.shape[0])
df1 = df1.head(limit)

df1.shape[0]


# --------------3 MONTH GAINERS-------------

# In[8]:


fcustom.set_filter(filters_dict=filters_dict3)
df3 = fcustom.screener_view(columns=cols, sleep_sec = 1,  order='Performance (Quarter)', ascend=False)
print(df3.shape[0])
df3 = df3.head(limit)

df3.shape[0]


# --------------6 MONTH GAINERS-------------

# In[9]:


fcustom.set_filter(filters_dict=filters_dict6)
df6 = fcustom.screener_view(columns=cols, sleep_sec = 1,  order='Performance (Half Year)', ascend=False)
print(df6.shape[0])

df6 = df6.head(limit)

df6.shape[0]


# --------------MERGE-------------

# In[10]:


df_final = pd.concat([df1, df3, df6], axis=0)


# In[11]:


df_final = df_final.drop_duplicates(subset=['Ticker'], keep='first')


# In[12]:


df_final.shape[0]


# In[15]:


s = set(df_final['Ticker'])


# In[16]:


set_to_tv(s)

