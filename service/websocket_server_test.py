#!/usr/bin/env python

import asyncio
from aioconsole import ainput
import websockets
import logging

logging.basicConfig()
logger = logging.getLogger("Test Server")
logger.setLevel(logging.DEBUG)

async def read(websocket):
    while True:
        t = await websocket.recv()
        logger.info(t)

async def write(websocket):
    while True:
        line = await ainput(">>>> ")

async def connection(websocket, path):
    logger.debug("Started Connection")
    while True:
        done, pending = await asyncio.wait(
            [ write(websocket), read(websocket)],
            return_when=asyncio.ALL_COMPLETED)

send_server = websockets.serve(connection, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(send_server)
asyncio.get_event_loop().run_forever()
