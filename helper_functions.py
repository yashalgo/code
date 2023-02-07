from libs import *
from paths import *

def instrument_token(data, symbol):
    """
    This function will return the token number of the instrument from data
    """
    return data[data.tradingsymbol == symbol].instrument_token.values[0]

def login_in_zerodha(api_key, api_secret, user_id, user_pwd, totp_key):
    driver = uc.Chrome()
    driver.get(f'https://kite.trade/connect/login?api_key={api_key}&v=3')
    login_id = WebDriverWait(driver, 10).until(lambda x: x.find_element("xpath",'//*[@id="userid"]'))
    login_id.send_keys(user_id)

    pwd = WebDriverWait(driver, 10).until(lambda x: x.find_element("xpath",'//*[@id="password"]'))
    pwd.send_keys(user_pwd)

    submit = WebDriverWait(driver, 10).until(lambda x: x.find_element("xpath",'//*[@id="container"]/div/div/div[2]/form/div[4]/button'))
    submit.click()

    time.sleep(1)
    #adjustment to code to include totp
    totp = WebDriverWait(driver, 10).until(lambda x: x.find_element("xpath",'//*[@label="External TOTP"]'))
    print(totp)
    authkey = pyotp.TOTP(totp_key)
    print(authkey.now())
    totp.send_keys(authkey.now())
    #adjustment complete

    continue_btn = WebDriverWait(driver, 10).until(lambda x: x.find_element("xpath",'//*[@id="container"]/div/div/div[2]/form/div[3]/button'))
    continue_btn.click()

    time.sleep(5)

    url = driver.current_url
    initial_token = url.split('request_token=')[1]
    request_token = initial_token.split('&')[0]

    driver.close()

    kite = KiteConnect(api_key = api_key)
    #print(request_token)
    data = kite.generate_session(request_token, api_secret=api_secret)
    kite.set_access_token(data['access_token'])

    return kite

def install_package(required):
    #required - a set of packages to be installed
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        python = sys.executable
        subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

def get_connection_info(file):
    try:
        with open('connection_info.json') as json_file:
            data = json.load(json_file)
    except:
        print('Error in loading data')
        return
        # Print the type of data variable
#         print("Type:", type(data))
    return data

#gDrive functions
def renameFile(drive, fileId, newTitle):
    a=drive.auth.service.files().get(fileId=id).execute()
    a['title']=newTitle
    update=drive.auth.service.files().update(fileId=id,body=a).execute()
    return update

def tv_str_to_list(s):
    x = s.replace('NSE:','').split(',')
    x.remove('Symbol')
    return x

def read_file_from_symbol(symbol, basedir = str(day_)):
    file = glob(basedir+'/*'+symbol+'*')[0]
    print(file)
    df = pd.read_csv(file)
    df['Date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x.split(' ')[0], '%Y-%m-%d'))
    df.drop(['Unnamed: 0', 'date'],inplace=True, axis=1)
    return df

def txt_to_str(fname):
    with open(fname, 'r') as file:
        data = file.read().replace('\n', '')
    return data

def read_file_from_symbol(symbol, basedir = str(day_)):
    file = glob(basedir+'/*'+symbol+'*')[0]
    print(file)
    df = pd.read_csv(file)
    df['Date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x.split(' ')[0], '%Y-%m-%d'))
    df.drop(['Unnamed: 0', 'date'],inplace=True, axis=1)
    return df

def read_file_from_symbol2(symbol, basedir = str(day_)):
    file = glob(basedir+'/'+symbol+'.csv')[0]
    print(file)
    df=pd.read_csv(file)[['Date','Open','High','Low','Close','Volume']]
    df.columns = ['Date','open','high','low','close','volume']
    df['Date'] = df['Date'].apply(lambda x: datetime.datetime.strptime(x.split(' ')[0], '%Y-%m-%d'))
    # df.drop(['Unnamed: 0'],inplace=True, axis=1)
    return df

def read_file_from_symbol3(symbol, basedir = str(day_)):
    file = glob(basedir+'/*'+symbol+'*')[0]
    print(file)
    df = pd.read_csv(file)
    df['Date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x.split('+')[0], '%Y-%m-%d %H:%M:%S'))
    df.drop(['Unnamed: 0', 'date'],inplace=True, axis=1)
    return df
    
def filter_df_dates(df, start_, end_):
    start_ = datetime.datetime.strptime(start_,'%Y%m%d')
    end_ = datetime.datetime.strptime(end_,'%Y%m%d')
    Q_df = df[(df['Date'] >= start_) & (df['Date'] <= end_)]
    return Q_df

def adr(df, period = 20):
    df['ADR%'] = ((df['high']/df['low']).rolling(period).mean() - 1) * 100
    return df

def n_month_gain(df, n):
    col_name = str(n)+'M_low'
    df[col_name] = df['low'].rolling(n * 22).min()
    # print(df.head())
    col_name2 = col_name + '_gain'
    df[col_name2] = (df['close']/df[col_name] - 1) * 100
    # df.drop(col_name, inplace = True)
    return df

def vwap(df):
    q = df.quantity.values
    p = df.price.values
    return df.assign(vwap=(p * q).cumsum() / q.cumsum())

def check_vols(df):
    if max(df.volume) <= 0:
        return False    
    return True

def typical_vwap(df):
    q = df.volume.values
    p = df.tp.values
    return df.assign(typical_vwap=(p * q).cumsum() / q.cumsum())

def save_plot(group, imgname):
    fig = go.Figure(data=[
                        go.Candlestick(
                            x=group['DateTime'],
                            open=group['open'],
                            high=group['high'],
                            low=group['low'],
                            close=group['close']),
                        go.Scatter(
                            x = group['DateTime'],
                            y = group['vwap'])
                        ])
    fig.update_xaxes(rangeslider_visible=False)
    # fig.update_yaxes(visible = False)
    fig.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    fig['data'][1]['line']['color']="#0000FF"
    fig.write_image(imgname + ".png")

def set_to_tv(s, outfile):
    s = {x.replace("&","_").replace("-","_") for x in s}
    tv_string = ','.join(list(s))
    with open(outfile, "w") as text_file:
        text_file.write(tv_string)
    print(outfile)

def set_to_tv2(s, outfile = datetime.today().strftime('%Y%m%d') + '_1_3_6_M_chartink.txt'):
    s = {x.replace("&","_").replace("-","_") for x in s}
    tv_string = ','.join(list(s))
    with open(outfile, "w") as text_file:
        text_file.write(tv_string)
    print(outfile)

def set_to_tv_US(s, outfile = datetime.today().strftime('%Y%m%d') + '_US.txt', exchange = 'NASDAQ'):
#     s = {exchange + ":" + x.replace("&","_").replace("-","_") for x in s}
    s = {x.replace("&","_").replace("-","_") for x in s}

    tv_string = ','.join(list(s))
    with open(outfile, "w") as text_file:
        text_file.write(tv_string)
    print(outfile)

def to_tv(infile):
    df = pd.read_csv(infile)
    df['tv_ticker'] = df['Security Name'].apply(lambda x: "NSE:" + x.replace("&","_").replace("-","_"))
    tv_string = ','.join(list(df['tv_ticker']))
    outfile = infile.replace('.csv','_tv.txt')
    with open(outfile, "w") as text_file:
        text_file.write(tv_string)
    print(outfile)