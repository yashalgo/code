from datetime import datetime
import pandas as pd
import os

today = datetime.today().strftime('%Y/%m/%d')
today2 = datetime.today().strftime('%Y%m%d')

def set_to_tv(s, outfile = today2 + '_Q_IND.txt', exchange = 'NSE'):
    s = {exchange + ":" + x.replace("&","_").replace("-","_") for x in s}
    tv_string = ','.join(list(s))
    with open(outfile, "w") as text_file:
        text_file.write(tv_string)
    print(outfile)

os.chdir('/Users/yash/Desktop/Trading/Q/watchlists/'+today)

#1-3-6 m gainers

s = set()

for i in [1,3,6]:
    df = pd.read_excel(str(i) + '.xlsx')
    print(df['Unnamed: 2'].shape)
    temp_set = set(df['Unnamed: 2'])
    set_to_tv(temp_set, outfile = today2 + '_' + str(i) + '_M_Q_IND.txt')
    s.update(temp_set)
print(len(s))
set_to_tv(s)