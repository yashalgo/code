from libs import *
from helper_functions import *

today = datetime.today().strftime('%Y/%m/%d')

os.chdir(vcp_wl / today)

df = pd.read_excel('VCP.xlsx')

today_ = datetime.today().strftime('%Y%m%d')

s = set()

print(df['Unnamed: 2'].shape)
s.update(set(df['Unnamed: 2']))
set_to_tv(s, today_ + '_VCP.txt')
