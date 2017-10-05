#!/usr/bin/env python

import asyncio
from aioconsole import ainput
import websockets
import logging

logging.basicConfig()
logger = logging.getLogger("Test Server")
logger.setLevel(logging.DEBUG)

async def read(websocket):
    logger.debug("Waiting for signal")
    t = await websocket.recv()
    logger.debug("ACKing")
    await websocket.send('["worker.connect",null,{"id":83758,"channel":null,"user_id":null,"success":true,"result":null,"token":null,"server_token":null}]')
    await websocket.send('["spawn",{"id":2,"script":"echo Hello Adam","working_directory":"~","environment_variables":"","timeout":null,"name":"Yes Abhishek","user_id":1,"created_at":"2017-10-04T20:42:14.689Z","updated_at":"2017-10-04T20:42:14.689Z"},{"id":null,"channel":"worker.5","user_id":null,"success":null,"result":null,"token":"01cddb65-bdd1-4227-901a-f3b161cc1858","server_token":null}]')
    logger.info(t)

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

        await asyncio.sleep(5)

send_server = websockets.serve(connection, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(send_server)
asyncio.get_event_loop().run_forever()
