from tracemalloc import start

import config
import alpaca_trade_api as tradeapi
from alpaca_trade_api.stream import Stream
import matplotlib.pyplot as plt
from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd
from datetime import date, datetime
import time
import talib


##############################################################
# Assign constant variables and use in the rest of the script.
##############################################################
# Ticker symbol and condition
ticker = "AMC"
condition = 0
crypto = "BTCUSD"
# Datetime object for reading the data
start_day1 = date.today().strftime('%Y-%m-%d')
start_time = start_day1 + ' 03:00:00 AM'
start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S %p')

# Account information
api_key = config.api_key
api_secret = config.api_secret
base_url = config.base_url
data_url = config.data_url
crypto_url = config.crypto_url
##############################################################
##############################################################

##############################################################
# Check the account information
##############################################################
try:
    api_account = REST(api_key, api_secret, base_url, api_version='v2')
    account = api_account.get_account()

    print(f'Cash status: {account.status}', end='\n')
    print(f'Cash available: {account.cash}', end='\n')
    print(f'Buying power: {account.buying_power}', end='\n')

    time.sleep(1)

except:

    print('Account authentication failed')
    time.sleep(1)
##############################################################
##############################################################

api_data = REST(api_key, api_secret, data_url, api_version='v2')

while condition == 0:

    time_now = datetime.now()#, '%d/%m/%y %H:%M:%S')

    duration = time_now - start_time 
    # print(duration)                  
    duration_in_1min = int(duration.total_seconds()//60) + 1
    duration_in_5min = int(duration.total_seconds()//300) + 1
    try:
        data5 = api_data.get_barset(ticker, timeframe = "5Min", start = start_day1, limit = duration_in_5min).df
        data1 = api_data.get_barset(ticker, timeframe = "1Min", start = start_day1, limit = duration_in_1min).df
    except:
        print('Data download failed.')
    
    data5.index = data5.index.tz_convert('US/Central')
    data5 = data5[data5.index >= start_day1]
    data1.index = data1.index.tz_convert('US/Central')
    data1 = data1[data1.index >= start_day1]


    # data1 = data1.resample('1Min').mean()
    # print(data1.isna())
    # data1['rsi'] = talib.RSI(data1["close"])
    # data5 = data5.resample('5Min').mean()
    # data5['rsi'] = talib.RSI(data5["close"])
    # print(data1)
    # print(data5.tail())
    # print(data1.shape)
    condition = 1
    # print(duration_in_min)
data1.to_csv('data.csv')
data1[ticker]['close'].plot()
plt.savefig('AMC.png')