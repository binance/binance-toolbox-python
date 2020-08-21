#!/usr/bin/env python

'''
Listens to the user's websocket and creates a fixed number of orders to list the Transaction vs Event time (T vs E)
and Event vs Received time (T vs Now) for every order update

python order-update-latency.py
'''

import asyncio
import logging
from binance.lib.utils import config_logging, get_timestamp
from binance.spot import Spot as Client
from binance.websocket.spot.websocket_client import SpotWebsocketClient
import json
import random

config_logging(logging, logging.INFO)

api_key = ''
api_secret = ''

# testnet
client = Client(api_key, api_secret, base_url='https://testnet.binance.vision')


def message_handler(message):
    if "executionReport" in json.dumps(message):
        print(f"Time diff >> "
              f"Order id:{message['data']['i']}, "
              f"Execution type:{message['data']['x']}, "
              f"Transaction vs Event time: {message['data']['E'] - message['data']['T']} ms, "
              f"Event vs Received time: {get_timestamp() - message['data']['E']} ms"
              )


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

    symbol = 'BNBUSDT'
    order_counter = 1

    params = {
        'symbol': symbol,
        'side': 'BUY',
        'type': 'LIMIT_MAKER',
        'quantity': round(random.uniform(0, 5), 2),
        'price': float(client.ticker_price(symbol)['price']) - round(random.uniform(0, 10), 2)
    }
    while order_counter <= 100:
        response = client.new_order(**params)
        logging.info("order ID: {}".format(response['orderId']))
        await asyncio.sleep(1)
        order_counter += 1

    # cancel all open orders
    client.cancel_open_orders(symbol)


def main():

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(listen_ws(), create_orders()))
    loop.close()


main()
