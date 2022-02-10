import config
import alpaca_trade_api as tradeapi
from alpaca_trade_api.stream import Stream
import matplotlib.pyplot as plt
from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd
from datetime import date, datetime
import time
from transformers import pipeline
import warnings
warnings.filterwarnings("ignore")

classifier = pipeline('sentiment-analysis')
# classifier = pipeline('sentiment-analysis')

ticker = 'SPY'

async def news_data_handler(news):

    news1 = news.pop()
    summary = news1.summary
    headline = news1.headline

    print('######################################################')
    print(f"Summary of the news: \n {headline}")
    print('######################################################')
    print(f"Summary of the news: \n {summary}")
    print('######################################################')

    relevant_text = summary + ' ' + headline
    sentiment = classifier(relevant_text)

    if sentiment[0]['label'] == 'POSITIVE' and sentiment[0]['score'] > 0.95:
        print('EXP news positive')
        # rest_client.submit_order("XPO", 100)
        
    elif sentiment[0]['label'] == 'NEGATIVE' and sentiment[0]['score'] > 0.95:
        print('EXP news negative')
        # rest_client.submit_order(XPO, -100)


#######################################################
# Account information
api_key = config.api_key
api_secret = config.api_secret
base_url = config.base_url
data_url = config.data_url
crypto_url = config.crypto_url
#######################################################

# rest_client = REST(api_key, api_secret)
# news = rest_client.get_news(ticker, start="2022-02-02", limit=1)

# news1 = news.pop()
# print(news1)
# summary = news1.summary
# headline = news1.headline

# print('######################################################')
# print(f"Headline of the news: \n {headline}")
# print('######################################################')
# print(f"Summary of the news: \n {summary}")
# print('######################################################')

# relevant_text = summary + ' ' + headline
# sentiment = classifier(relevant_text)

# print(sentiment[0])

# if sentiment[0]['label'] == 'POSITIVE' and sentiment[0]['score'] > 0:
#     print('EXP news positive')
#     # rest_client.submit_order("XPO", 100)
    
# elif sentiment[0]['label'] == 'NEGATIVE' and sentiment[0]['score'] > 0:
#     print('EXP news negative')
    # rest_client.submit_order(XPO, -100)

print('\n')
print('\n')
print(f'Waiting for the news for {ticker} ...')
print('\n')
print('\n')

stream_client = Stream(api_key, api_secret)
stream_client.subscribe_news(news_data_handler, ticker)
stream_client.run()

