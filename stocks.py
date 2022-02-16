from tracemalloc import start
import yfinance as yf
import config
import alpaca_trade_api as tradeapi
from alpaca_trade_api.stream import Stream
import matplotlib.pyplot as plt
from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd
from datetime import date, datetime
import time
import talib
import numpy as np

import warnings
warnings.filterwarnings("ignore")


##############################################################
# Assign constant variables and use in the rest of the script.
##############################################################
# Initialization and constants
ticker = "SOFI" # Ticker symbol(s) that we are checking.
buy = False # This boolean variable indicates that whether an order is filled/submitted or not.
RIS_up = 70
RIS_low = 30
percent_gain = 0.5 # Once every trade hits the percent gain, it generates a sell signal to liquidate the position and realize the gain.
N = 10000 # The amount spent in dollars for buying or selling a security.

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

except:
    print('Account authentication failed')
##############################################################
##############################################################

api_data = REST(api_key, api_secret, data_url, api_version='v2')

condition = 0

while condition == 0:

    if time.localtime().tm_sec%6 == 0:
        
        time1 = time.time()

        time_now = datetime.now()#, '%d/%m/%y %H:%M:%S')

        duration = time_now - start_time 
        # print(duration)                  
        duration_in_1min = int(duration.total_seconds()//60) + 1
        duration_in_5min = int(duration.total_seconds()//300) + 1
        try:
            df2 = api_data.get_bars(ticker, timeframe = "1Min", start = start_day1, limit = duration_in_1min).df.tz_convert('US/Central')
            df2 = df2[(df2.index >= start_day1) & (df2.index < '08:30:00')]
            df2.index.names = ['DateTime']
            df2.drop(['trade_count', 'vwap'], axis = 1, inplace = True)

            df1 = yf.download(ticker, start=start_day1, interval='1m').tz_convert('US/Central')
            df1.drop(['Adj Close'], axis = 1, inplace = True)
            df1.columns = ['open', 'high','low', 'close', 'volume']
        except:
            print('Morning data downloader failed.')

        try:
            data1 = df2.append(df1, ignore_index=False)

            df2 = api_data.get_bars(ticker, timeframe = "5Min", start = start_day1, limit = duration_in_5min).df.tz_convert('US/Central')
            df2 = df2[(df2.index >= start_day1) & (df2.index < '08:30:00')]
            df2.index.names = ['DateTime']
            df2.drop(['trade_count', 'vwap'], axis = 1, inplace = True)

            df1 = yf.download(ticker, start=start_day1, interval='5m').tz_convert('US/Central')
            df1.drop(['Adj Close'], axis = 1, inplace = True)
            df1.columns = ['open', 'high','low', 'close', 'volume']

            data5 = df2.append(df1, ignore_index=False)
        except:
            print('Intraday data downloader failed.')
        
        
        try:
            data1['rsi'] = talib.RSI(data1["close"])
            data5['rsi'] = talib.RSI(data5["close"])
            print(f'RSI is at {np.round(data5.rsi.iloc[-1], 2)}')
            print(f'Execution time: {(time.time() - time1)} seconds')
            
            if data5.rsi[-1] < RIS_low:
                if not buy:
                    api_account.submit_order(
                        symbol=ticker,
                        side='buy',
                        type='market',
                        qty=np.round(N/data1.close[-1]),
                        time_in_force='day',
                    )
                    buy = True
                    print(f"Buy signal at {time.strftime('%H:%M:%S')} ")
                    print(f'Buy {np.round(N/data1.close[-1])} of {ticker} at {np.round(data1.close[-1], 2)}.')
                    
                    position = api_data.get_position(ticker)
                    cost_basis = position.avg_entry_price
                    quantity = position.qty


            elif data5.rsi[-1] > RIS_up:
                print(f"Sell signal at {time.strftime('%H:%M:%S')} ")
            
            try:
                if (data1.close[-1] >= (1 + percent_gain/100) * cost_basis):
                    print(f"Sell signal at {time.strftime('%H:%M:%S')} ")

                    if buy:
                        api_account.submit_order(
                            symbol=ticker,
                            side='sell',
                            type='market',
                            qty= quantity,
                            time_in_force='day',
                        )
                        buy = False
                        print(f"Sell signal at {time.strftime('%H:%M:%S')} ")
                        print(f'Sell {quantity} of {ticker} at {np.round(data1.close[-1], 2)}.')
            except:
                pass

        except:
            print('Loop not complete.')
