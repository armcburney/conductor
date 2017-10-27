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
from health_check.health_check_coroutine import HealthCheckCoroutine
from process_wrapper_command import ProcessWrapperCommand
from command_handlers.command_handler_factory import CommandHandlerFactory


logging.basicConfig(filename='slave_master.log', level=logging.DEBUG)
logging.addLevelName( logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName( logging.INFO, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.INFO))
logging.addLevelName( logging.DEBUG, "\033[1;34m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))
logging.addLevelName( logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

logger = logging.getLogger("Slave Manager")
logger.setLevel(logging.DEBUG)

debug = logger.debug
warning = logger.warning
error = logger.error
info = logger.info

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
        self.pending_children = []

    async def process_command(self, websocket):
        """
        Process a command in an actor like fashion
        """

        # keep on processing commands while available
        command = await websocket.recv()

        debug("Parsing raw command: {}".format(command))
        response = ResponseFactory.parse_response(command)

        # if the command is invalid, just ignore it
        if response is None:
            warning("Could not recognize command. Ignoring")
            return

        handler = CommandHandlerFactory.get_handler(response)

        if handler is None:
            warning("Couldn't find handler for command.")
            return

        handler.handle(response)

        debug("Successfully processed command")

    def clean_pending_children(self):
        # cleanup children who are still pending
        self.pending_children = list(
            filter(lambda x: not x.done(), self.pending_children)
        )

    async def initiate_connection(self, websocket, reconnect=False):

        # Determine if we want to reconnect with the same host id
        if reconnect:
            command = ConnectCommand(api_key=self.api_key, node_id=self.node_id)
        else:
            command = RegisterNode(api_key=self.api_key)

        # Send registration command
        debug("Sending registration request")
        await websocket.send(str(command))

        # wait for response
        debug("Waiting for connection response")
        response = await websocket.recv()
        parsed_response = ResponseFactory.parse_response(response)

        if not parsed_response or \
           not type(parsed_response) == WorkerConnectedResponse or \
           not parsed_response.success:
            return False

        debug("Waiting for registration response")
        registration_response = await websocket.recv()
        parsed_register_response = ResponseFactory.parse_response(registration_response)

        if not parsed_register_response or \
           not type(parsed_register_response) == RegisterNodeResponse:
            return False

        debug("Successfully registered with master server: {}".format(parsed_register_response.node_id))

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

                    # get the initial connection response
                    response = await websocket.recv()
                    parsed_response = ResponseFactory.parse_response(response)

                    # this is the expected first response
                    if not (type(parsed_response) is ClientConnectedResponse):
                        error("Got unexpected initial response: {}".format(type(parsed_response)))

                        # can't expect this sequence to be valid, try reconnecting
                        raise Exception()

                    # Try to register node
                    try:
                        # register this node with the main server
                        debug("Trying to register with host")

                        if not await self.initiate_connection(websocket, reconnect=reconnect):
                            # this connection attempt failed
                            continue

                        # At this point in time we are guaranteed to be registered

                        # Schedule the health check
                        debug("Starting health check")
                        self.health_check_coroutine = asyncio.ensure_future(
                            HealthCheckCoroutine(
                                api_key=self.api_key,
                                node_id=self.node_id
                            ).run(websocket)
                        )

                        # keep on processing commands from the server while possible
                        while websocket.open:
                            await asyncio.ensure_future(self.process_command(websocket))
                    except:
                        # print debugging info
                        traceback.print_exc()
                        raise

                debug("Websocket dead")

                # If we have retried the max amount of times, then stop trying to reconnect with the same id
                if num_reconnect_tries < MAX_RECONNECT_TRIES:
                    num_reconnect_tries += 1
                    reconnect = True
                else:
                    reconnect = False

            except:
                debug("Error occured, sleeping before trying to reconnect")
                time.sleep(1)


if __name__ == "__main__":

    parser = ArgumentParser(
        "Main communication endpoint on worker host. "
        "Spawn to communicate with Conductor service."
    )

    parser.add_argument(
        "--token",
        dest="token",
        action="store",
        required=True,
        help="Provided api token from Conductor web service."
    )

    parser.add_argument(
        "--service_host",
        dest="service_host",
        action="store",
        required=True,
        help="The service master to connect to.",
    )

    arguments = parser.parse_args()

    # create an instance of the manager
    slave_manager = SlaveManager(
        api_key=arguments.token,
        service_host=arguments.service_host,
    )

    # continually run event loop to process coroutines
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(slave_manager.run())
