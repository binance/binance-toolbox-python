#!/usr/bin/env python

import time
from binance.spot import Spot as Client

key = ''
secret = ''

# For testnet
# client = Client(key, secret, base_url='https://testnet.binance.vision')

# For production
client = Client(key, secret)

symbol = 'BTCUSDT'

while True:
    # Post a new order
    params = {
        'symbol': symbol,
        'side': 'BUY',
        'type': 'LIMIT_MAKER',
        'quantity': 0.002,
        'price': 9000
    }

    response = client.new_order(**params)
    print("order created with order ID: {}".format(response['orderId']))

    # Cancel the order
    response = client.cancel_order(symbol, orderId=response['orderId'])

    print("order cancelled for : {}".format(response['orderId']))
    time.sleep(1)
