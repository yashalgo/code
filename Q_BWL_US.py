#!/usr/bin/env python
# coding: utf-8

# #Creates backwatchlist set for watchlists from last friday to most recent thursday => watchlists for all trading days for last trading week
from libs import *
from helper_functions import *

today = date.today() - timedelta(days=70)
latest_monday = today + timedelta(days=-today.weekday())

print(today, latest_monday)

dateset = set()

for i in range(5):
    d = latest_monday + timedelta(days=i)
    ds = d.strftime('%Y%m%d')
    dateset.add(ds)

os.chdir('/Users/yash/Desktop/Trading/Q/watchlists')

files = glob('**/*US.txt', recursive = True)

ticker_set = set()

for f in files:
    ds = f.split('/')[-1].split('_')[0]
    if ds in dateset:
        print(ds)
        with open(f, 'r') as file:
            data = file.read().replace('\n', '')
        data = data.split(',')
        ticker_set.update(set(data))
print(len(ticker_set))

os.chdir('/Users/yash/Desktop/Trading/Q/backwatchlists/')

outfile = latest_monday.strftime('%Y%m%d') + '_' + datetime.today().strftime('%Y%m%d') + '_BWL_US.txt'
set_to_tv(ticker_set, outfile)