from tracemalloc import start
import config
import alpaca_trade_api as tradeapi
from alpaca_trade_api.stream import Stream
import matplotlib.pyplot as plt
from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd
from datetime import date, datetime
import time


##############################################################
# Assign constant variables and use in the rest of the script.
##############################################################
# Ticker symbol and condition
ticker = "AMC"
condition = 0

# Datetime object for reading the data
start_day1 = date.today().strftime('%Y-%m-%d')
start_time = start_day1 + ' 03:00:00 AM'
start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S %p')

# Account information
api_key = config.api_key
api_secret = config.api_secret
base_url = config.base_url
data_url = config.data_url
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
    duration_in_min = int(duration.total_seconds()//60) + 1
    data = api_data.get_bars(ticker, timeframe = "1Min", start = start_day1, limit = duration_in_min, adjustment = 'raw').df
    print(type(data))
    data.index = data.index.tz_convert('US/Central')
    data = data.resample('1Min').mean()
    # print(duration_in_min)

    # 
    condition = 1


# data.to_csv('data.csv')
# data['close'].plot()
# plt.savefig('AMC.png')

print(data.head())
print('\n')
print(data.tail())

