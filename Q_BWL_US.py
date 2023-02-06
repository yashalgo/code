#!/usr/bin/env python
# coding: utf-8

# #Creates backwatchlist set for watchlists from last friday to most recent thursday => watchlists for all trading days for last trading week

# In[2]:


from datetime import date,datetime, timedelta
import pandas as pd
import os
from glob import glob


# In[3]:


def set_to_tv(s, outfile):
    s = {x.replace("&","_").replace("-","_") for x in s}
    tv_string = ','.join(list(s))
    with open(outfile, "w") as text_file:
        text_file.write(tv_string)
    print(outfile)


# In[4]:


today = date.today() - timedelta(days=70)
latest_monday = today + timedelta(days=-today.weekday())


# In[5]:


print(today, latest_monday)

# In[6]:

dateset = set()


# In[7]:


for i in range(5):
    d = latest_monday + timedelta(days=i)
    ds = d.strftime('%Y%m%d')
    dateset.add(ds)


# In[8]:


os.chdir('/Users/yash/Desktop/Trading/Q/watchlists')


# In[9]:


files = glob('**/*US.txt', recursive = True)


# In[10]:


ticker_set = set()


# In[11]:


for f in files:
    ds = f.split('/')[-1].split('_')[0]
    if ds in dateset:
        print(ds)
        with open(f, 'r') as file:
            data = file.read().replace('\n', '')
        data = data.split(',')
        ticker_set.update(set(data))
print(len(ticker_set))


# In[12]:


os.chdir('/Users/yash/Desktop/Trading/Q/backwatchlists/')


# In[13]:
outfile = latest_monday.strftime('%Y%m%d') + '_' + today.strftime('%Y%m%d') + '_BWL_US.txt'
set_to_tv(ticker_set, outfile)


# In[ ]:




