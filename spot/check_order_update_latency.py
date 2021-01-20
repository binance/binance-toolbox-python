#!/usr/bin/env python

"""
Listens to the user's websocket and creates a fixed number of orders to list the Transaction vs Event time (T vs E)
and Event vs Received time (T vs Now) for every order update

Instructions:
0. pip install binance-connector-python
1. Set your own environment variables (BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_SECRET_KEY, BINANCE_SYMBOL):
2. python check_order_update_latency.py

"""

import asyncio
import logging
from binance.lib.utils import config_logging, get_timestamp
from binance.spot import Spot as Client
from binance.websocket.spot.websocket_client import SpotWebsocketClient
import json
import random
import os


config_logging(logging, logging.INFO)

# testnet
client = Client(os.getenv('BINANCE_TESTNET_API_KEY'),
                os.getenv('BINANCE_TESTNET_SECRET_KEY'),
                base_url='https://testnet.binance.vision')

symbol = os.getenv('BINANCE_SYMBOL')


def message_handler(message):
    if "executionReport" in json.dumps(message):
        print(f"Time diff >> "
              f"Order id:{message['data']['i']}, "
              f"Execution type:{message['data']['x']}, "
              f"TvsE: {message['data']['E'] - message['data']['T']} ms, "
              f"EvsNow: {get_timestamp() - message['data']['E']} ms"
              )


def get_min_notion():
    for s in client.exchange_info().get('symbols'):
        if s.get('symbol') == symbol:
            return float(s['filters'][3]['minNotional'])


def get_parameters(min_notional):

    quantity = round(random.uniform(1, 5), 2)
    price = round(float(client.ticker_price(symbol)['price']) - random.uniform(0, 5), 2)

    params = {
        'symbol': symbol,
        'side': 'BUY',
        'type': 'LIMIT_MAKER',
        'quantity': quantity,
        'price': price if (price * quantity) > min_notional else round((min_notional + 1 / quantity), 2)
    }
    print(params)
    return params


async def listen_ws():

    response = client.new_listen_key()
    logging.info(f"Receiving listen key : {response['listenKey']}")

    ws_client = SpotWebsocketClient(stream_url='wss://testnet.binance.vision')
    ws_client.start()
    ws_client.user_data(
        listen_key=response['listenKey'],
        id=1,
        callback=message_handler,
    )

    logging.debug("closing ws connection")
    # ws_client.stop()


async def create_orders():

    # Finalise websocket subscription
    await asyncio.sleep(1)

    order_counter = 1
    max_orders = 100  # Optional
    min_notional = get_min_notion()

    while order_counter <= max_orders:
        response = client.new_order(**get_parameters(min_notional))
        logging.info("order ID: {}".format(response['orderId']))
        await asyncio.sleep(1)
        order_counter += 1

    # Cancel all open orders
    client.cancel_open_orders(symbol)


def main():

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(listen_ws(), create_orders()))
    loop.close()


main()
