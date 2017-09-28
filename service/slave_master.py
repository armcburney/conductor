import os
import threading
import time
import asyncio
import logging
import json

from argparse import ArgumentParser
from websocket_adapter import RegisterNode, HealthCommand

import websockets
import psutil

logging.basicConfig()
logger = logging.getLogger("Slave Main")
logger.setLevel(logging.DEBUG)

class ServerHealth:
    """
    Encapsulate data pertaining to the current health of the server.
    """

    def __init__(
        self,
        cpu_count,
        user_load,
        system_load,
        total_memory,
        available_memory,
        total_disk,
        used_disk,
        free_disk
    ):
        self.cpu_count = cpu_count
        self.user_load = user_load
        self.system_load = system_load
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

        # TODO: add network statistics

        return ServerHealth(
            cpu_count=cpu_count,
            user_load=cpu_util.user,
            system_load=cpu_util.system,
            total_memory=virtual_memory.total,
            available_memory=virtual_memory.available,
            total_disk=disk_usage.total,
            used_disk=disk_usage.used,
            free_disk=disk_usage.free,
        )

    def serialize(self):
        return json.dumps({
            "cpu_count": self.cpu_count,
            "user_load": self.user_load,
            "system_load": self.system_load,
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

        logger.debug("Logging node health")
        health = HealthCommand(self.get_server_health().serialize())
        logger.debug("Sending server health")
        await websocket.send(str(health))
        logger.debug("Sent health status")


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

    async def process_command(self, websocket):

        # keep on processing commands while available
        command = await websocket.recv()

        logger.debug("Processing command: {}".format(command))

    async def spawn_worker_wrapper(self, command, args):
        """
        Get a command to spawn a worker process.
        """
        logging.debug("Spawning wrapper")
        # need yield from because not fully compatible yet
        process = await asyncio.create_subprocess_exec(command, *args, stderr=asyncio.subprocess.PIPE)
        await process.wait()
        logging.debug("Wrapper completed")

    async def initiate_connection(self, websocket):
        command = RegisterNode({"address": self.hostname, "api_key": self.api_key})
        await websocket.send(str(command))
        response = await websocket.recv()
        logger.debug("Successfully associated")

    async def run(self):

        # keep a connection to a websocket while we're alive
        while True:

            # try:
            # connects to websocket on host
            async with websockets.connect(self.service_host) as websocket:

                # register this node with the main server
                logger.debug("Initiating connection")
                await self.initiate_connection(websocket)

                # schedule the reporter coroutine
                self.health_check_coroutine = asyncio.ensure_future(HealthCheckCoroutine().run(websocket))

                # keep on processing commands while possible
                while websocket.open:
                    await asyncio.ensure_future(self.process_command(websocket))

            logger.debug("Websocket dead")
            # except:
                # logger.debug("Error occured, sleeping")
                # time.sleep(1)

if __name__ == "__main__":

    parser = ArgumentParser("Main communication endpoint on server. Spawn to communicate with Conductor service.")

    parser.add_argument(
        "--token",
        dest="token",
        action="store",
        required=True,
        help="Provided api service token from Conductor."
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
        help="The unique hostname this service should register as."
    )

    arguments = parser.parse_args()

    slave_manager = SlaveManager(
        hostname=arguments.hostname,
        api_key=arguments.token,
        service_host=arguments.service_host,
    )

    asyncio.get_event_loop().run_until_complete(slave_manager.run())
