from libs import *
from helper_functions import *
from paths import *

today = datetime.today().strftime('%Y/%m/%d')
today2 = datetime.today().strftime('%Y%m%d')

os.chdir(q_wl  / today)

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