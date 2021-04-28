"""
Simple Script to obtain margin account's trades, based on:
https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-trade-list-user_data

Instructions:
1. Set up your account's api key as BINANCE_API_KEY environment variable;
2. Set up your account's api secret key as BINANCE_API_SECRET environment variable;
3. python get_my_trades.py
"""

import time
import requests
import hashlib
import hmac
from urllib.parse import urlencode, urljoin
import os

key = os.getenv('BINANCE_API_KEY')
secret = os.getenv('BINANCE_API_SECRET')
base_url = 'https://api.binance.com'

def signature(params):
    params_query_string = urlencode(params)
    return hmac.new(secret.encode('utf-8'), params_query_string.encode('utf-8'), hashlib.sha256).hexdigest()


def request(url, params):
    headers = {'X-MBX-APIKEY': key}
    response = requests.get(url, headers=headers, params=params)
    print(response.json())


# Request my account's trades
parameters = {
    'symbol': 'ETHUSDT',
    'limit': 500,
    'recvWindow': 10000,
    'timestamp': time.time_ns() // 1000000,
}

parameters['signature'] = signature(parameters)
url = urljoin(base_url, '/sapi/v1/margin/myTrades')
request(url, parameters)

