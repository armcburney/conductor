#!/usr/bin/python

import os
import threading
import time
import asyncio
import logging
import json

from argparse import ArgumentParser
from websocket_requests import RegisterNode, HealthCommand, ConnectCommand
from websocket_responses import ResponseFactory, SpawnResponse, ConnectNodeResponse, RegisterNodeResponse

import websockets
import psutil
import traceback

logging.basicConfig()
logger = logging.getLogger("Slave Main")
logger.setLevel(logging.DEBUG)

MAX_RECONNECT_TRIES=10

class ServerHealth:
    """
    Encapsulate data pertaining to the current health of the server.
    """

    def __init__(
        self,
        cpu_count,
        load,
        total_memory,
        available_memory,
        total_disk,
        used_disk,
        free_disk
    ):
        self.cpu_count = cpu_count
        self.load = load
        self.total_memory = total_memory
        self.available_memory = available_memory
        self.total_disk = total_disk
        self.used_disk = used_disk
        self.free_disk = free_disk

    @staticmethod
    def create():
        cpu_count = psutil.cpu_count(logical=True)
        cpu_util = psutil.cpu_times_percent()
        virtual_memory = psutil.virtual_memory()
        disk_usage = psutil.disk_usage("/")

        return ServerHealth(
            cpu_count=cpu_count,
            load=os.getloadavg(),
            total_memory=virtual_memory.total,
            available_memory=virtual_memory.available,
            total_disk=disk_usage.total,
            used_disk=disk_usage.used,
            free_disk=disk_usage.free,
        )

    def serialize(self):
        return json.dumps({
            "cpu_count": self.cpu_count,
            "load": self.load,
            "total_memory": self.total_memory,
            "available_memory": self.available_memory,
            "total_disk": self.total_disk,
            "used_disk": self.used_disk,
            "free_disk": self.free_disk,
        })


class HealthCheckCoroutine():
    """
    Periodically poll the system and send stats to the master.
    """

    def __init__(self, interval=10):
        self.interval = interval

    def get_server_health(self):
        return ServerHealth.create()

    async def send_stats(self, websocket):

        health = HealthCommand(self.get_server_health().serialize())
        logger.debug("Sending Server Health Status")
        await websocket.send(str(health))
        logger.debug("Sent Server Health Status")


    async def run(self, websocket):
        logger.debug("Starting health check coroutine.")

        # keep sending stats forever
        while websocket.open:

            await self.send_stats(websocket)

            # sleep for some timeout
            await asyncio.sleep(self.interval)

class SlaveManager():
    """
    Spawn wrapper processes when a new command is received.
    """

    def __init__(
        self,
        hostname,
        api_key,
        service_host,
    ):

        self.hostname = hostname
        self.service_host = service_host
        self.api_key = api_key

        # to be set based on the response from the server
        self.node_id = None

    async def process_command(self, websocket):

        # keep on processing commands while available
        command = await websocket.recv()

        logger.debug("Processing command: {}".format(command))

        response = ResponseFactory.parse_response(command)

        if type(response) is SpawnResponse:
            # spawn a job
            logger.debug("Got a Spawn command")
            await self.spawn_command(response)
        elif type(response) is ConnectNodeResponse:
            logger.debug("Got an unexpected Connect command")
        elif type(response) is RegisterNodeResponse:
            logger.debug("Got an unexpected Register command")
        else:
            logger.debug("Could not recognize command.")

        logger.debug("Successfully processed command")

    async def spawn_command(self, command):
        """
        Get a command to spawn a worker process.
        """
        # will clean up once we introduce python classes for responses
        process = await asyncio.create_subprocess_shell(
            os.path.join(command.script),
            stderr=asyncio.subprocess.PIPE
        )
        # NOTE: right now we don't wait for child to finish
        # await process.wait()
        logger.debug("Finished waiting")

    async def initiate_connection(self, websocket):
        command = RegisterNode(address=self.hostname, api_key=self.api_key)

        # Send registration command
        await websocket.send(str(command))
        response = await websocket.recv()

        parsed_response = ResponseFactory.parse_response(response)
        if not parsed_response is RegisterNodeResponse:
            logger.error("Unable to register host with master server")
            return

        self.node_id = parsed_response.node_id

        logger.debug("Successfully registered with master server")

    async def reinitiate_connection(self, websocket):
        command = ConnectCommand(api_key=self.api_key, node_id=self.node_id, address=self.hostname)

        # Send connection command
        await websocket.send(str(command))
        response = await websocket.recv()

        parsed_response = ResponseFactory.parse_response(response)
        if not type(parsed_response) is ConnectNodeResponse:
            logger.error("Unable to connect to master server")
            return

        logger.info("Successfully connected to the master server")

    async def run(self):
        num_reconnect_tries = 0 # how many times we've tried to reconnect
        reconnect = False

        # keep a connection to a websocket while we're alive
        while True:

            try:
                # connects to websocket on host
                async with websockets.connect(self.service_host) as websocket:
                    try:
                        # register this node with the main server
                        logger.debug("Initiating connection")
                        if not reconnect:
                            await self.initiate_connection(websocket)
                        else:
                            await self.reinitiate_connection(websocket)

                        # schedule the reporter coroutine
                        self.health_check_coroutine = asyncio.ensure_future(HealthCheckCoroutine().run(websocket))

                        # keep on processing commands while possible
                        while websocket.open:
                            await asyncio.ensure_future(self.process_command(websocket))
                    except:
                        traceback.print_exc()
                        raise

                logger.debug("Websocket dead")

                if num_reconnect_tries < MAX_RECONNECT_TRIES:
                    num_reconnect_tries += 1
                    reconnect = True
                else:
                    reconnect = False
            except:
                logger.debug("Error occured, sleeping before trying to reconnect")
                time.sleep(1)


if __name__ == "__main__":

    parser = ArgumentParser("Main communication endpoint on worker host. Spawn to communicate with Conductor service.")

    parser.add_argument(
        "--token",
        dest="token",
        action="store",
        required=True,
        help="Provided api token from Conductor."
    )

    parser.add_argument(
        "--service_host",
        dest="service_host",
        action="store",
        required=True,
        help="The service master to connect to.",
    )

    parser.add_argument(
        "--hostname",
        dest="hostname",
        action="store",
        required=True,
        help="The unique hostname this node should register itself as."
    )

    arguments = parser.parse_args()

    slave_manager = SlaveManager(
        hostname=arguments.hostname,
        api_key=arguments.token,
        service_host=arguments.service_host,
    )

    # continually run event loop
    asyncio.get_event_loop().run_until_complete(slave_manager.run())
