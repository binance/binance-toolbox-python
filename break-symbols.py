#!/usr/bin/env python

''' List all symbol in BREAK status

python break-symbols.py

'''

from binance.spot import Spot as Client

key = ''
secret = ''
# for production
client = Client(key, secret)

response = client.exchange_info()

for symbol in response['symbols']:
    s = symbol['symbol']
    if symbol['status'] == 'BREAK':
        print(s)

# print(response)
