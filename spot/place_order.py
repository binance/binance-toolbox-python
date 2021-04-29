#!/usr/bin/env python

"""
A simple script to place an order and cancel it every second.
Feel free to adjust the parameters or change from Testnet to Production setting.

Instructions:
    1. Have binance-connector-python installed
    2. Set up your account's api key as BINANCE_API_KEY environment variable
    3. Set up your account's api secret key as BINANCE_API_SECRET environment variable
    4. Define symbol in this file and adjust other fields if needed;
    5. python place_order.py

Note:
    Make sure to respect exchangeInfo endpoint's filters for price and quantity:
    https://binance-docs.github.io/apidocs/spot/en/#filters

"""

import os
import time
from binance.spot import Spot as Client


key = os.getenv('BINANCE_API_KEY')
secret = os.getenv('BINANCE_API_SECRET')


# For Testnet
client = Client(key, secret, base_url='https://testnet.binance.vision')

# # For Production
# client = Client(key, secret)

symbol = ''  # Example: BNBUSDT

while True:
    # Create an order and cancel the same order every second
    params = {
        'symbol': symbol,
        'side': 'BUY',
        'type': 'LIMIT_MAKER',
        'quantity': 10,
        'price': 1.35
    }

    response = client.new_order(**params)
    print("Created order ID: {}".format(response['orderId']))

    # Cancel the order
    response = client.cancel_order(symbol, orderId=response['orderId'])
    print("Canceled order ID: {}".format(response['orderId']))

    time.sleep(1)
