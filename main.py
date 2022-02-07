from tracemalloc import start
import config
import alpaca_trade_api as tradeapi
from alpaca_trade_api.stream import Stream
import matplotlib.pyplot as plt
from alpaca_trade_api.rest import REST
import pandas as pd
from datetime import date
import time


##############################################################
# Assign constant variables and use in the rest of the script.
##############################################################
ticker = 'AMC'
condition = 0
start_day = date.today()
api_key = config.api_key
api_secret = config.api_secret
base_url = config.base_url
##############################################################
##############################################################

##############################################################
# Check the account information
##############################################################
try:
    api = REST(api_key, api_secret, base_url, api_version='v2')
    account = api.get_account()

    print(f'Cash status: {account.status}', end='\n')
    print(f'Cash available: {account.cash}', end='\n')
    print(f'Buying power: {account.buying_power}', end='\n')

    time.sleep(5)

except:

    print('Account authentication failed')
    time.sleep(5)
##############################################################
##############################################################

while condition == 0:
    
    data = REST.get_bars(symbol = ticker,
                        timeframe = tradeapi.TimeFrameUnit.Minute,
                        adjustment='raw')


    condition = 1

print(data.tail())

