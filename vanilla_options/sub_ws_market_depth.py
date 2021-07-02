#!/usr/bin/env python

"""
A simple script to receive market depth updates through websocket for X secs

Instructions:
    python sub_ws_market_depth.py
"""

import websockets
import asyncio
import json
import gzip
import time

base_endpoint = 'wss://vstream.binance.com/ws/'
my_id = 123
sub_stream = 'BTC-210730-50000-C@depth100'
secs = 10  # How many seconds to monitor the events


async def monitor():

    t_end = time.time() + secs

    async with websockets.connect(base_endpoint) as ws:
        print('Websocket connection established! Subscribing to stream...')
        payload = json.dumps({
            'method': 'SUBSCRIBE',
            'params': [sub_stream],
            'id': my_id
        })
        await ws.send(payload)
        while time.time() < t_end:
            try:
                resp = await asyncio.wait_for(ws.recv(), timeout=10)
                data = gzip.decompress(resp)
                print(data.decode('UTF-8'))  # decode bytes into a string
            except asyncio.TimeoutError:
                print('No response after 5s: timeout!')


def run():

    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(monitor())


run()
