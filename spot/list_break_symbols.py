#!/usr/bin/env python

"""
Lists all symbols in BREAK status
python list_break_symbols.py
"""

from binance.spot import Spot as Client

key = ''
secret = ''

# For production
client = Client(key, secret)

response = client.exchange_info()

for symbol in response['symbols']:
    s = symbol['symbol']
    if symbol['status'] == 'BREAK':
        print(s)

# print(response)
