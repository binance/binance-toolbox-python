"""
Subscribes to 2 market streams and prints out their updates with associated symbols.

Instructions:
    1. Have binance-connector installed
    2. Define symbol_1 and symbol_2 in this file and adjust other stream subscription fields if needed
    3. python multi_subs_market_ws.py
"""

import asyncio
import logging
import time

from binance.lib.utils import config_logging
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient

symbol_1 = 'btcusdt'
symbol_2 = 'ethusdt'

config_logging(logging, logging.DEBUG)

def msg_handler(_, message):
    logging.info(f"{message}\n")

my_client = SpotWebsocketStreamClient(
    on_message=msg_handler,
    is_combined=True,
)

async def monitor():
    """Subscribes to 2 partial book depth market streams for 2 symbols:
    https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams#partial-book-depth-streams
    """
    my_client.partial_book_depth(symbol=f"{symbol_1}", level=5, speed=1000)
    my_client.partial_book_depth(symbol=f"{symbol_2}", level=5, speed=1000)
    time.sleep(10)
    my_client.stop()


def run():
    asyncio.run(monitor())


run()
