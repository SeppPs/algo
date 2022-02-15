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