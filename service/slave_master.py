#!/usr/bin/python

import os
import time
import asyncio
import logging

import traceback
import websockets

from argparse import ArgumentParser
from websocket_requests import RegisterNode, ConnectCommand
from websocket_responses import ResponseFactory, SpawnResponse, ClientConnectedResponse, RegisterNodeResponse, WorkerConnectedResponse
from health_check_coroutine import HealthCheckCoroutine


logging.basicConfig()
logger = logging.getLogger("Slave Main")
logger.setLevel(logging.DEBUG)

MAX_RECONNECT_TRIES=10

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

        # process_wrapper = str(ProcessWrapperCommand(command.id, command.script))
        # logger.info("Running command: {}".format(process_wrapper))

        # will clean up once we introduce python classes for responses
        process = await asyncio.create_subprocess_shell(
            # process_wrapper,
            command.script,
            cwd=command.working_directory,
            env=command.environment_variables,
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
                        logger.debug("Starting health check")
                        self.health_check_coroutine = asyncio.ensure_future(HealthCheckCoroutine(logger=logger).run(websocket))

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
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(slave_manager.run())
