from sys import api_version
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
ticker = "DWAC" # Ticker symbol(s) that we are checking.
buy = False # This boolean variable indicates that whether an order is filled/submitted or not.
RIS_up = 70
RIS_low = 30
percent_gain = 0.5 # Once every trade hits the percent gain, it generates a sell signal to liquidate the position and realize the gain.
N = 10000 # The amount spent in dollars for buying or selling a security.

# Datetime object for reading the data
# start_day1 = date.today().strftime('%Y-%m-%d')
# start_time = start_day1 + ' 03:00:00 AM'
# start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S %p')

# Account information
api_key = config.api_key
api_secret = config.api_secret
base_url = config.base_url
data_url = config.data_url
crypto_url = config.crypto_url
##############################################################
async def trade_callback(t):
    print(t)

    try:
        if ('F' in t.conditions)and (t.size > 500) and (not api_account.list_positions()):
            api_account.submit_order(
                            symbol=ticker,
                            side='buy',
                            type='market',
                            qty=np.round(500/t.price),
                            time_in_force='day',
                        )
            time.sleep(0.4)
            api_account.submit_order(
                        symbol=ticker,
                        side='sell',
                        type='trailing_stop',
                        trail_price = 0.25,
                        qty=np.round(500/t.price)
                            )

            print('##################################')
            print(t)
            print(f'Sweep order of {t.size} shares detected at {t.timestamp}')
            print(f'Order type: {t.conditions}')
            print(f'Price at {t.price}')

            w = str(t.size) + ' , ' +  str(t.price) + ' , ' + str(t.timestamp) + ' , ' + t.symbol + '\n'
            with open('large_orders' + ticker + '.txt', 'a') as file:
                file.write(w)
                file.close()


    except:
        print('Order not filled')
        # time.sleep(1)
        # position = api_account.get_position(ticker)
        # cost_basis = position.avg_entry_price
        # quantity = position.qty
        
        # api_account.submit_order(
        #                 symbol=ticker,
        #                 side='sell',
        #                 type='limit',
        #                 limit_price= np.round(cost_basis*1.003),
        #                 qty=quantity,
        #                 time_in_force='day',
        #             )
        # print('Orders were submitted')

# async def quote_callback(q):
#     # print('quote', q)
#     if q.ask_size - q.bid_size >= 10:
#         print(f'Buy signal is generate at {np.round((q.ask_price), 2)}')
#         print(f'Difference is {q.ask_size - q.bid_size} at     {q.timestamp}')
#         print('\n')
#     if q.ask_size - q.bid_size <= -10:
#         print(f'Sell signal is generate at {np.round((q.bid_price), 2)}')
#         print(f'Difference is {q.ask_size - q.bid_size} at     {q.timestamp}')
#         print('\n')
##############################################################

try:
    api_account = REST(api_key, api_secret, base_url, api_version='v2')
    account = api_account.get_account()
    print('##################################')
    print('ACCOUNT INFORMATION:')
    print(f'Cash status: {account.status}', end='\n')
    print(f'Cash available: {account.cash}', end='\n')
    print(f'Buying power: {account.buying_power}', end='\n')
    print('##################################')

except:
    print('Account authentication failed')


stream = Stream(api_key,
            api_secret,
            base_url=base_url,
            data_feed='sip')

stream.subscribe_trades(trade_callback, ticker)
# stream.subscribe_quotes(quote_callback, ticker)
print('\n \n \n')
print('Start:')
print('##################################')
stream.run()