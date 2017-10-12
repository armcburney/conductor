#!/usr/bin/env python

import asyncio
from aioconsole import ainput
import websockets
import logging

logging.basicConfig()
logger = logging.getLogger("Test Server")
logger.setLevel(logging.DEBUG)

async def read(websocket):
    t = await websocket.recv()
    logger.info('Received: {}'.format(t))

async def write(websocket):
    line = await ainput(">>>> ")
    await websocket.send(line)

async def connection(websocket, path):
    logger.debug("Started Connection")
    while websocket.open:
        done, pending = await asyncio.wait(
            [write(websocket), read(websocket)],
            return_when=asyncio.FIRST_COMPLETED)
        for future in pending:
            future.cancel()

send_server = websockets.serve(connection, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(send_server)
asyncio.get_event_loop().run_forever()
