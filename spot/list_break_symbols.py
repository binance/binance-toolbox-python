#!/usr/bin/env python

"""
Lists all symbols in production that's with BREAK status

Instructions:
    python list_break_symbols.py
"""

from binance.spot import Spot as Client

# For production
client = Client()

response = client.exchange_info()

for symbol in response['symbols']:
    s = symbol['symbol']
    if symbol['status'] == 'BREAK':
        print(s)
