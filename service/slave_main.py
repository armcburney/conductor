#!/usr/bin/python3

import os
import threading
import time
import asyncio
import logging

from argparse import ArgumentParser

import websockets
import subprocess
import psutil


class ServerHealth:
    """
    Encapsulate data pertaining to the current health of the server.
    """

    def __init__(self):
        self.cpu_count = psutil.cpu_count()
        self.cpu_freq = psutil.cpu_freq()
        self.cpu_util = psutil.cpu_times_percent()
        self.disk_usage = psutil.disk_usage()
        self.network_usage = psutil.net_io_counters()
        self.virtual_memory = psutil.virtual_memory()
        self.swap_memory = psutil.swap_memory()


class HealthCheckThread(threading.Thread):
    """
    Periodically poll the system and send stats to the master.
    """

    def __init__(self, interval=10):
        self.interval = interval

    def get_server_health(self,):
        return ServerHealth()

    def send_stats(self, health):
        print (health)
        print ("TODO: implement")

    def run():
        while(True):
            self.send_stats(self.get_server_health())

            # sleep for some timeout
            time.sleep(self.interval)

class SlaveManager():
    """
    Spawn wrapper processes when a new command is received.
    """

    def __init__(
        self,
        hostname,
        api_token,
        service_host,
        service_port,
    ):

        self.hostname = hostname
        self.service_host = service_host
        self.service_port = service_port
        self.api_token = api_token

        # Create thread to be used for checking health of our server
        self._health_check_thread = threading.Thread()

    async def process_command(self):
        pass

    def spawn_worker_wrapper(self,):
        """
        Get a command to spawn a worker process.
        """
        pass

    async def initiate_connection(self, websocket):
        await websocket.send("000:{}".format(self.hostname))
        response = await websocket.recv()

        # TODO: handle the error code and possibly recover

    async def run(self):

        # Start thread to send periodic health checks to the Conductor service
        self._health_check_thread.start()

        # connects to websocket on host
        async with websockets.connect(self.service_host) as websocket:
            await self.initiate_connection(websocket)

            while (True):
                # keep on processing commands while available
                command = await websocket.recv()
                logging.debug("Processing command: {}".format(command))
                await self.process_command(command)

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
        "--service_port",
        dest="service_port",
        default=80,
        help="The port on the service master to connect to. Defaults to 80.",
    )

    parser.add_argument(
        "--hostname",
        dest="hostname",
        action="store",
        required=True,
        help="The unique hostname this service should register as."
    )

    parser.parse_args()

    slave_manager = SlaveManager(
        hostname=parser.hostname,
        api_token=parser.token,
        service_host=parser.service_host,
        service_port=parser.service_port,
    )

    asyncio.get_event_loop().run_until_complete(slave_manager.run())
