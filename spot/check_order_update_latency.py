#!/usr/bin/env python

"""
Incrementally creates order every second while listening to the account's websocket to check the
Transaction vs Event time (T vs E) and Event vs Received time (T vs Now) for every received order update.
Processes ends when 5 orders is reached and all open orders are canceled.

T - time the transaction happened
E - time the payload was created
Now - time the payload was received locally

Instructions:
    1. Have binance-connector-python installed
    2. Set up your account's api key as BINANCE_API_KEY environment variable
    3. Set up your account's api secret key as BINANCE_API_SECRET environment variable
    4. Define symbol in this file and adjust other fields if needed;
    5. python check_order_update_latency.py

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

# Testnet
client = Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_API_SECRET'),
                base_url='https://testnet.binance.vision')
ws_client = SpotWebsocketClient(stream_url='wss://testnet.binance.vision')

symbol = ''  # Example: BNBUSDT


def message_handler(message):
    if "executionReport" in json.dumps(message):
        print(f"Time diff >> "
              f"Order id:{message['data']['i']}, "
              f"Execution type:{message['data']['x']}, "
              f"TvsE: {message['data']['E'] - message['data']['T']} ms, "
              f"EvsNow: {get_timestamp() - message['data']['E']} ms"
              )


def get_parameters():

    quantity = 10
    price = float(client.ticker_price(symbol)['price'])

    params = {
        'symbol': symbol,
        'side': 'BUY',
        'type': 'LIMIT_MAKER',
        'quantity': quantity,
        'price': price
    }
    return params


async def listen_ws():

    response = client.new_listen_key()
    logging.info("Starting ws connection")
    ws_client.start()
    ws_client.user_data(
        listen_key=response['listenKey'],
        id=1,
        callback=message_handler,
    )


async def create_orders():

    # Time to finalise websocket connection set up
    await asyncio.sleep(1)

    order_counter = 1
    max_orders = 5  # Optional

    while order_counter <= max_orders:
        params = get_parameters()
        response = client.new_order(**params)
        logging.info(f"Created order id {response['orderId']} with params: {params})")
        await asyncio.sleep(1)
        order_counter += 1

    # Cancel all open orders
    client.cancel_open_orders(symbol)
    logging.info("closing ws connection")
    ws_client.stop()


def main():

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(listen_ws(), create_orders()))
    loop.close()


main()
