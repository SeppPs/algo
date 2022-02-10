# Algorithmic Trading

This code aims to create an algorithmic trading program than runs based off of Alpaca-trading API.
The data are provided by combining yahoo finance data provider and Alpaca API.

## Methodology

- Create a dataset and calculate relative strength index (RSI) indicator using ta-lib package.
- On the 5-min chart, once RSI drops below 30, RSI-check module turns off.
- Order book check module is turned on and it starts checking minor movements in the price action.
- Once huge buy orders are detected in the order book, a buy order signal is triggered.
- An order of certain size is submitted to the Alpaca API.
- Once the order is filled, RSI-check module and order book check module looks for a profitable exit.
- TBC...
