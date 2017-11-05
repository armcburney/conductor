#!/usr/bin/python

import asyncio
from argparse import ArgumentParser
import logging
import signal
import sys
import time
import traceback
import websockets

logging.basicConfig(level=logging.DEBUG)
logging.addLevelName( logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName( logging.INFO, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.INFO))
logging.addLevelName( logging.DEBUG, "\033[1;34m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))
logging.addLevelName( logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
logging.addLevelName( logging.CRITICAL, "\033[1;92m%s\033[1;0m" % logging.getLevelName(logging.CRITICAL))

logger = logging.getLogger("Worker Manager")
logger.setLevel(logging.DEBUG)

from websocket_requests import RegisterNode, ConnectCommand
from websocket_responses import ResponseFactory, SpawnResponse, ClientConnectedResponse, RegisterNodeResponse, WorkerConnectedResponse, ClientKillResponse
from health_check.health_check_coroutine import HealthCheckCoroutine
from command_handlers.command_handler_factory import CommandHandlerFactory
from global_commands import *


MAX_RECONNECT_TRIES=10

class WorkerManager():
    """
    Spawn wrapper processes when a new command is received.
    """

    def __init__(
        self,
        api_key,
        service_host,
    ):

        self.health_check_coroutine = None
        self.service_host = service_host
        self.api_key = api_key

        # to be set based on the response from the server
        self.node_id = None

        # jobs which have been spawned and havent finished
        self.pending_children = []

    def get_state_dict(self):
        return {
            "service_host": self.service_host,
            "api_key": self.api_key,
            "node_id": self.node_id,
            "pending_children": self.pending_children
        }

    async def process_command(self, websocket):
        """
        Process a command in an actor like fashion
        """

        # get a command
        command = await websocket.recv()

        logger.debug("Parsing command: %s", command)

        # if the command is invalid, just ignore it
        response = ResponseFactory.parse_response(command)
        if response is None:
            logger.warning("Could not recognize command. Ignoring")
            return

        # find the appropriate handler for this job
        handler = CommandHandlerFactory.get_handler(response)
        if handler is None:
            logger.warning("Couldn't find handler for command.")
            return

        # execute the command based on our current state
        task = await handler.handle(**self.get_state_dict())

        # add this task to the waiting list
        self.pending_children.append(task)

        logger.info("Processed request")

    def clean_pending_children(self):
        # cleanup children who are still pending
        original_pending_tasks = len(self.pending_children)
        self.pending_children = list(
            filter(lambda x: not x.done(), self.pending_children)
        )

        new_pending_tasks = len(self.pending_children)

        if original_pending_tasks > new_pending_tasks:
            logger.debug(
                "Cleaned up finished tasks from pending list."
                " Before: %d tasks, After: %d tasks",
                original_pending_tasks,
                new_pending_tasks,
            )

    async def initiate_connection(self, websocket, reconnect=False):

        # Determine if we want to reconnect with the same host id
        # Tightly coupled but I think it makes sense here
        if reconnect:
            command = ConnectCommand(api_key=self.api_key, node_id=self.node_id)
            logger.info("Sending reconnection request")
        else:
            command = RegisterNode(api_key=self.api_key)
            logger.info("Sending registration request")

        # Send registration command
        await websocket.send(str(command))

        # wait for response
        logger.debug("Waiting for connection response")
        response = await websocket.recv()
        parsed_response = ResponseFactory.parse_response(response)

        if not parsed_response or \
           not isinstance(parsed_response, WorkerConnectedResponse) or \
           not parsed_response.success:
            return False

        logger.debug("Waiting for registration response")
        registration_response = await websocket.recv()
        parsed_register_response = ResponseFactory.parse_response(registration_response)

        if not parsed_register_response or \
           not isinstance(parsed_register_response, RegisterNodeResponse):
            return False

        logger.info("Registered with master server: Worker ID={}".format(parsed_register_response.node_id))

        self.node_id = parsed_register_response.node_id

        return True

    async def run(self):

        num_reconnect_tries = 0 # how many times we've tried to reconnect
        reconnect = False # whether to try reconnecting with the same id

        # keep a connection to a websocket while we're alive
        while True:

            # If we have retried the max amount of times,
            # then stop trying to reconnect with the same id
            if num_reconnect_tries < MAX_RECONNECT_TRIES:
                reconnect = True
            else:
                reconnect = False

            try:

                # connects to websocket on host
                async with websockets.connect(self.service_host) as websocket:

                    # get the initial connection response
                    response = await websocket.recv()
                    parsed_response = ResponseFactory.parse_response(response)

                    # this is the expected first response
                    if not (type(parsed_response) is ClientConnectedResponse):
                        logger.error("Got unexpected initial response: %s", type(parsed_response))

                        # can't expect this sequence to be valid, try reconnecting
                        raise Exception()

                    # Try to register node
                    try:
                        # register this node with the main server
                        logger.debug("Trying to register with host")

                        if not await self.initiate_connection(websocket, reconnect=reconnect):
                            num_reconnect_tries += 1
                            # this connection attempt failed
                            continue

                        # we are connected, reset retry counter
                        num_reconnect_tries = 0

                        # At this point in time we are guaranteed to be registered

                        # Schedule the health check
                        logger.debug("Starting health check")
                        self.health_check_coroutine = asyncio.ensure_future(
                            HealthCheckCoroutine(
                                api_key=self.api_key,
                                node_id=self.node_id
                            ).run(websocket)
                        )

                        # keep on processing commands from the server while possible
                        while websocket.open:
                            self.clean_pending_children()
                            await asyncio.ensure_future(self.process_command(websocket))

                    except Kill:

                        def alarm_handler(signum, frame):
                            logger.critical("Timeout, killing remaining tasks and raising exception")
                            for task in self.pending_children:
                                if not task.done():
                                    task.kill_process()

                            raise TimeoutError()

                        logger.info("Stopping tasks")

                        # send SIGSTOP to children
                        for task in self.pending_children:
                            await task.stop_process()

                        # setup timeout alarm
                        signal.signal(signal.SIGALRM, alarm_handler)
                        signal.alarm(10)

                        # check that all things stopped
                        for task in self.pending_children:
                            await task.wait()
                            logger.debug("Killed task %s", task)

                        # reset alarm so it doesn't fail
                        signal.alarm(0)

                        raise

                    except:
                        # print debugging info
                        traceback.print_exc()
                        raise

                logger.debug("Websocket dead")

            except Kill:
                logger.info("Shutting down node.")
                sys.exit(0)

            except:
                if self.health_check_coroutine:
                    self.health_check_coroutine.cancel()
                    self.health_check_coroutine = None

                logger.info("Error occured, sleeping before trying to reconnect")
                time.sleep(10)


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
    worker_manager = WorkerManager(
        api_key=arguments.token,
        service_host=arguments.service_host,
    )

    # continually run event loop to process coroutines
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(worker_manager.run())
