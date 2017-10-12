#!/usr/bin/python

import os
import threading
import time
import asyncio
import logging
import json

from argparse import ArgumentParser
from websocket_requests import RegisterNode, HealthCommand, ConnectCommand
from websocket_responses import ResponseFactory, SpawnResponse, ClientConnectedResponse, RegisterNodeResponse, WorkerConnectedResponse

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

    def to_dict(self):
        return {
            "cpu_count": self.cpu_count,
            "load": self.load,
            "total_memory": self.total_memory,
            "available_memory": self.available_memory,
            "total_disk": self.total_disk,
            "used_disk": self.used_disk,
            "free_disk": self.free_disk,
        }



class HealthCheckCoroutine():
    """
    Periodically poll the system and send stats to the master.
    """

    def __init__(self, interval=10):
        self.interval = interval

    def get_server_health(self):
        return ServerHealth.create()

    async def send_stats(self, websocket):

        health = HealthCommand(self.get_server_health().to_dict())
        logger.debug("Sending Server Health Status")
        logger.debug(str(health))
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
        api_key,
        service_host,
    ):

        self.service_host = service_host
        self.api_key = api_key

        # to be set based on the response from the server
        self.node_id = None

    async def process_command(self, websocket):

        # keep on processing commands while available
        command = await websocket.recv()

        logger.debug("Processing command: {}".format(command))

        response = ResponseFactory.parse_response(command)
        logger.debug("Got Response with type: {}".format(type(response)))

        if type(response) is SpawnResponse:
            # spawn a job
            logger.debug("Got a Spawn command")
            await self.spawn_command(response)
        elif type(response) is ClientConnectedResponse:
            logger.debug("Got an unexpected Connect command")
        elif type(response) is RegisterNodeResponse:
            logger.debug("Got an unexpected Register command")
        else:
            logger.debug("Could not recognize command.")
            return

        logger.debug("Successfully processed command")

    async def spawn_command(self, command):
        """
        Get a command to spawn a worker process.
        """

        class ProcessWrapperCommand():
            def __init__(self, job_id, command):
                self.job_id = job_id
                self.command = command

            def __str__(self):
                return f"python process_wrapper.py --command=\"{self.command}\" --job_id={self.job_id}"

        process_wrapper = str(ProcessWrapperCommand(command.id, command.script))
        logger.info("Running command: {}".format(process_wrapper))

        # will clean up once we introduce python classes for responses
        process = await asyncio.create_subprocess_shell(
            process_wrapper,
            stderr=asyncio.subprocess.PIPE
        )
        # NOTE: right now we don't wait for child to finish
        # await process.wait()

    async def initiate_connection(self, websocket, reconnect=False):

        # Determine if we want to reconnect with the same host id
        if reconnect:
            command = ConnectCommand(api_key=self.api_key, node_id=self.node_id)
        else:
            command = RegisterNode(api_key=self.api_key)

        # Send registration command
        logger.debug("Sending registration request")
        await websocket.send(str(command))

        # wait for response
        logger.debug("Waiting for connection response")
        response = await websocket.recv()
        parsed_response = ResponseFactory.parse_response(response)

        if not parsed_response or \
           not type(parsed_response) == WorkerConnectedResponse or \
           not parsed_response.success:
            return False

        logger.debug("Waiting for registration response")
        response2 = await websocket.recv()
        parsed_register_response = ResponseFactory.parse_response(response2)

        if not parsed_register_response or \
           not type(parsed_register_response) == RegisterNodeResponse:
            return False

        logger.debug("Successfully registered with master server: {}".format(parsed_register_response.node_id))

        self.node_id = parsed_register_response.node_id

        return True

    async def run(self):

        num_reconnect_tries = 0 # how many times we've tried to reconnect
        reconnect = False # whether to try reconnecting with the same id

        # keep a connection to a websocket while we're alive
        while True:

            try:

                # connects to websocket on host
                async with websockets.connect(self.service_host) as websocket:

                    # get the initial Connect response
                    response = await websocket.recv()
                    parsed_response = ResponseFactory.parse_response(response)

                    if not (type(parsed_response) is ClientConnectedResponse):
                        logger.error("Got unexpected initial response: {}".format(type(parsed_response)))

                        # can't expect this sequence to be valid, try reconnecting
                        raise Exception()

                    # Try to register node
                    try:
                        # register this node with the main server
                        logger.debug("Trying to register with host")

                        if not await self.initiate_connection(websocket, reconnect=reconnect):
                            # this connection attempt failed
                            continue

                        # At this point in time we are guaranteed to be registered

                        # Schedule the health check
                        self.health_check_coroutine = asyncio.ensure_future(HealthCheckCoroutine().run(websocket))

                        # keep on processing commands from the server while possible
                        while websocket.open:
                            await asyncio.ensure_future(self.process_command(websocket))
                    except:
                        traceback.print_exc()
                        raise

                logger.debug("Websocket dead")

                # If we have retried the max amount of times, then stop trying to reconnect with the same id
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

    arguments = parser.parse_args()

    slave_manager = SlaveManager(
        api_key=arguments.token,
        service_host=arguments.service_host,
    )

    # continually run event loop
    asyncio.get_event_loop().run_until_complete(slave_manager.run())
