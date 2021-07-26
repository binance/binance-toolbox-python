"""
Subscribes to 2 market streams and prints out their updates with associated symbols.

Instructions:
    1. Have binance-connector installed
    2. Define symbol_1 and symbol_2 in this file and adjust other stream subscription fields if needed
    3. python multi_subs_market_ws.py
"""

from binance.websocket.spot.websocket_client import SpotWebsocketClient
import asyncio
import json

ws_client = SpotWebsocketClient()

symbol_1 = 'btcusdt'
symbol_2 = 'ethusdt'


def msg_handler_1(message):
    print(f'{symbol_1} {json.dumps(message)}')


def msg_handler_2(message):
    print(f'{symbol_2} {json.dumps(message)}')


async def monitor():
    """Subscribes to 2 partial book depth market streams for 2 symbols:
    https://binance-docs.github.io/apidocs/spot/en/#partial-book-depth-streams
    """
    ws_client.start()
    ws_client.partial_book_depth(
        symbol=symbol_1,
        id=123,
        callback=msg_handler_1,
        level=5,
        speed=1000
    )
    ws_client.partial_book_depth(
        symbol=symbol_2,
        id=321,
        callback=msg_handler_2,
        level=5,
        speed=1000
    )


def run():
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(monitor())


run()
