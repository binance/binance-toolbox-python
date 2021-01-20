"""
Listens user's data stream and creates 3 requests to obtain user's position.

Instructions:
1. Set your own environment variable BINANCE_LISTEN_KEY
2. python test_user_data_stream.py
"""


import websockets
import asyncio
import json
from datetime import datetime
import os

listenKey = os.getenv('BINANCE_LISTEN_KEY')
stream_endpoint = f'wss://dstream.binance.com/ws/{listenKey}'
request_name = '@position'
my_id = 123


async def monitor():
    counter = 0
    async with websockets.connect(stream_endpoint) as ws:
        while True:
            payload = json.dumps({
                'method': 'REQUEST',
                'params': [f'{listenKey}{request_name}'],
                'id': my_id
            })

            print('Send @position request', datetime.now().strftime("%H:%M:%S"))
            await ws.send(payload)
            try:
                resp = json.loads(await asyncio.wait_for(ws.recv(), timeout=10))
                if 'id' in resp:
                    print(datetime.now().strftime("%H:%M:%S"), f'Received response with id={resp.get("id")}')
                else:
                    # Not request's response but pushed event update
                    print(datetime.now().strftime("%H:%M:%S"), f'Received Event update')
                    pass
            except asyncio.TimeoutError:
                print('No response after 10s: timeout!')

            # Wait 3s to send next request
            await asyncio.sleep(3)

            # Finish after sending 3 requests
            counter += 1
            if counter == 3:
                break


def run():

    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(monitor())


run()
