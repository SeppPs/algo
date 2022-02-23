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



################################################################################################################
class Crypto_Bot:

    def __init__(self, trades, tickers = 'BTCUSD', order_amount = 500):

        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.tickers = tickers
        self.trades = trades
        self.order_amount = order_amount
        try:
            print('Account authentication')
            self.api_account = REST(self.api_key, self.api_secret, self.base_url, api_version='v2')
            self.account = self.api_account.get_account()
        except:
            print('Account authentication failed')

    def account_info(self):
        print('#############################')
        print('ACCOUNT INFORMATION:')
        print(f'Cash status: {self.account.status}', end='\n')
        print(f'Cash available: {self.account.cash}', end='\n')
        print(f'Buying power: {self.account.buying_power}', end='\n')
        print('#############################')


    def large_sweep_detection(self):

        if 'F' in self.trades.condition:
            print('##################################')
            print(t)
            print(f'Sweep order of {t.size} shares detected at {t.timestamp}')
            print(f'Order type: {t.conditions}')
            print(f'Price at {t.price}')

    
    def submit_order(self):

        self.api_account.submit_order(
                        symbol=self.ticker,
                        side='buy',
                        type='market',
                        qty=np.round(),
                        time_in_force='day',
                    )

    

################################################################################################################
api_key = config.api_key
api_secret = config.api_secret
base_url = config.base_url

bot = Crypto_Bot(api_key, api_secret, base_url, tickers = 'BTCUSD',  order_amount = 2000)
bot.account_info()

async def trade_callback(t):

    if ('F' in t.conditions):

        print('##################################')
        print(t)
        print(f'Sweep order of {t.size} shares detected at {t.timestamp}')
        print(f'Order type: {t.conditions}')
        print(f'Price at {t.price}')



stream = Stream(api_key,
            api_secret,
            base_url=base_url)

ticker = 'BTCUSD'
stream.subscribe_trades(trade_callback, ticker)
# stream.subscribe_quotes(quote_callback, ticker)
print('\n \n \n')
print('Start:')
print('##################################')
stream.run()