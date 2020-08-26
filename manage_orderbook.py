#!/usr/bin/env python

from binance.spot import Spot as Client
from binance.websocket.spot.websocket_client import SpotWebsocketClient
from binance.lib.utils import config_logging
import os
import logging
import json
import asyncio

"""
Creates, manages a local orderbook and prints out its best prices.
Based on https://binance-docs.github.io/apidocs/spot/en/#diff-depth-stream

Instructions:
0.pip install binance-connector-python
1.Set your own environment variables (BINANCE_TESTNET_API_KEY, BINANCE_TESTNET_SECRET_KEY, BINANCE_SYMBOL,
                                      BINANCE_BASE_URL, BINANCE_STREAM_URL):
  Production:
  BINANCE_BASE_URL='https://api.binance.com', BINANCE_STREAM_URL='wss://stream.binance.com:9443/ws'
  Testnet:
  BINANCE_BASE_URL='https://testnet.binance.vision', BINANCE_STREAM_URL='wss://testnet.binance.vision/ws'
  
2.python manage-orderbook.py

"""

config_logging(logging, logging.INFO)

client = Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_SECRET_KEY'), base_url=os.getenv('BINANCE_BASE_URL'))
symbol = os.getenv('BINANCE_SYMBOL')
orderbook = {}


def get_snapshot():
    """
    Retrieve orderbook
    """
    return client.depth(symbol, limit=1000)


def manage_orderbook(side, update):
    """
    Updates local orderbook's bid or ask lists based on the received update ([price, quantity])
    """

    price, quantity = update

    # price exists: remove or update local order
    for i in range(0, len(orderbook[side])):
        if price == orderbook[side][i][0]:
            # quantity is 0: remove
            if float(quantity) == 0:
                orderbook[side].pop(i)
                return
            else:
                # quantity is not 0: update the order with new quantity
                orderbook[side][i] = update
                return

    # price not found: add new order
    if float(quantity) != 0:
        orderbook[side].append(update)
        if side == 'asks':
            orderbook[side] = sorted(orderbook[side])  # asks prices in ascendant order
        else:
            orderbook[side] = sorted(orderbook[side], reverse=True)  # bids prices in descendant order

        # maintain side depth <= 1000
        if len(orderbook[side]) > 1000:
            orderbook[side].pop(len(orderbook[side]) - 1)


def process_updates(message):
    """
    Updates bid and ask orders in the local orderbook.
    """

    for update in message['b']:
        manage_orderbook('bids', update)
    for update in message['a']:
        manage_orderbook('asks', update)


def message_handler(message):
    """
    Creates and checks sync of local orderbook with depthUpdate message's u (Final update ID in event)
    and U (First update ID in event). If synced, then the message will be processed.
    """

    global orderbook

    if "depthUpdate" in json.dumps(message):

        if not orderbook:
            orderbook = get_snapshot()

        last_update_id = orderbook['lastUpdateId']

        if message['u'] <= last_update_id:
            return  # Not an update, wait for next message
        if message['U'] <= last_update_id + 1 <= message['u']:
            orderbook['lastUpdateId'] = message['u']
            process_updates(message)
        elif message['U'] == last_update_id + 1:
            orderbook['lastUpdateId'] = message['u']
            process_updates(message)
        else:
            logging.info('Out of sync, abort')


async def listen_ws():
    """
    Listens to the ws to get the updates messages.
    """

    response = client.new_listen_key()
    ws_client = SpotWebsocketClient(stream_url=f'{os.getenv("BINANCE_STREAM_URL")}/{symbol.lower()}@depth')

    ws_client.start()
    ws_client.user_data(
        listen_key=response['listenKey'],
        id=1,
        callback=message_handler,
    )

    logging.debug("closing ws connection")
    # ws_client.stop()


async def get_best_price():
    """
    Gets best available prices (for bid and ask).
    """

    while True:
        if orderbook:
            print(f'Best price > bid:{orderbook["bids"][0][0]} , ask:{orderbook["asks"][0][0]}')
        await asyncio.sleep(1)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(listen_ws(), get_best_price()))
    loop.close()


main()
