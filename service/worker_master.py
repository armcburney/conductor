#!/usr/bin/python

import asyncio
from argparse import ArgumentParser
import logging
import sys
import time
import traceback
from typing import Iterable
import websockets

from defaults import *

logging.basicConfig(level=logging.DEBUG)
logging.addLevelName( logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName( logging.INFO, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.INFO))
logging.addLevelName( logging.DEBUG, "\033[1;34m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))
logging.addLevelName( logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
logging.addLevelName( logging.CRITICAL, "\033[1;92m%s\033[1;0m" % logging.getLevelName(logging.CRITICAL))

logger = logging.getLogger("Worker Manager")
logger.setLevel(logging.DEBUG)

logging.getLogger('asyncio').propagate = False
logging.getLogger('websockets.protocol').propagate = False

from websocket_requests import RegisterNode, ConnectCommand
from websocket_responses import ResponseFactory, SpawnResponse, ClientConnectedResponse, RegisterNodeResponse, WorkerConnectedResponse, ClientKillResponse
from health_check.health_check_coroutine import HealthCheckCoroutine
from command_handlers.command_handler_factory import CommandHandlerFactory
from global_commands import *
from process_wrapper_command import ProcessWrapperCommand

MAX_RECONNECT_TRIES=10

class WebsocketConnectionError(Exception):
        pass

class WorkerManager():
    """
    Spawn wrapper processes when a new command is received.
    """

    def __init__(
            self,
            api_key: str,
            service_host: str,
    ) -> None:

        self.service_host = service_host
        self.api_key = api_key

        # to be set based on the response from the server
        self.node_id = None

        # jobs which have been spawned and havent finished
        self.pending_children = []
        self.num_reconnect_tries = 0 # how many times we've tried to reconnect

    def get_state_dict(self):
        """
        Returns the current state of this coroutine.
        """
        return {
            "service_host": self.service_host,
            "api_key": self.api_key,
            "node_id": self.node_id,
            "pending_children": self.pending_children,
            "num_reconnect_tries": self.num_reconnect_tries
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
            return None

        # find the appropriate handler for this job
        handler = CommandHandlerFactory.get_handler(response)
        if handler is None:
            logger.warning("Couldn't find handler for command.")
            return None

        # execute the command based on our current state
        # add this task to the waiting list
        return await handler.handle(**self.get_state_dict())

    @staticmethod
    def clean_pending_children(pending_children):
        # cleanup children who are still pending
        original_pending_tasks = len(pending_children)
        pending_children = list(
            filter(lambda x: not x.done(), pending_children)
        )

        new_pending_tasks = len(pending_children)

        if original_pending_tasks > new_pending_tasks:
            logger.debug(
                "Cleaned up finished tasks from pending list."
                " Before: %d tasks, After: %d tasks",
                original_pending_tasks,
                new_pending_tasks,
            )

        return pending_children

    @staticmethod
    async def stop_all_children(
            pending_children: Iterable
    ):
        pending_children = WorkerManager.clean_pending_children(pending_children)
        logger.info("Stopping tasks")

        #try to gracefully stop
        try:
            # send SIGSTOP to children
            for task in pending_children:
                await task.stop_process()

            # check that all things stopped
            for task in pending_children:
                await asyncio.wait_for(task.wait(), timeout=10)
                logger.debug("Killed task %s", task)
        except asyncio.TimeoutError:
            logger.critical("Timeout, killing remaining tasks.")
            for task in pending_children:
                if not task.done():
                    task.kill_process()

    @staticmethod
    async def registration(
            websocket: websockets.client.WebSocketClientProtocol,
            api_key: str,
            node_id=None
    ):
        """
        Register perform the registration flow with the provided parameters

        Params:
            websocket: websocket to use for connection
            api_key: api_key to send to register with
            node_id: id to try reconnecting ask
        """

        # Determine if we want to reconnect with the same host id
        # Tightly coupled but I think it makes sense here
        if node_id:
            command = ConnectCommand(api_key=api_key, node_id=node_id)
            logger.info("Sending reconnection request")
        else:
            command = RegisterNode(api_key=api_key)
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
            raise WebsocketConnectionError()

        logger.debug("Waiting for registration response")
        registration_response = await websocket.recv()
        parsed_register_response = ResponseFactory.parse_response(registration_response)

        if not parsed_register_response or \
           not isinstance(parsed_register_response, RegisterNodeResponse):
            raise WebsocketConnectionError()

        logger.info("Registered with master server: Worker ID=%s", parsed_register_response.node_id)

        return parsed_register_response.node_id

    @staticmethod
    async def pre_registration(
            websocket: websockets.client.WebSocketClientProtocol
    ):
        """
        Performs pre_registration connection flow.
        """

        # get the initial connection response
        response = await websocket.recv()
        parsed_response = ResponseFactory.parse_response(response)

        # this is the expected first response
        if not isinstance(parsed_response, ClientConnectedResponse):
            logger.error("Got unexpected initial response: %s", type(parsed_response))

            # can't expect this sequence to be valid, fail
            raise WebsocketConnectionError()

        # we're connected

    async def register_and_process(
            self,
            websocket: websockets.client.WebSocketClientProtocol,
            reconnect: bool
    ):

        health_check_coroutine = None
        pending_children = []

        await self.pre_registration(websocket)

        # Try to register node
        try:
            # register this node with the main server
            logger.debug("Trying to register with host")

            #will fail hard
            self.node_id = await self.registration(
                websocket=websocket,
                api_key=self.api_key,
                node_id=self.node_id if reconnect else None
            )

            # we are connected, reset retry counter
            self.num_reconnect_tries = 0

            # At this point in time we are guaranteed to be registered

            # Schedule the health check
            health_check_coroutine = asyncio.ensure_future(
                HealthCheckCoroutine(
                    api_key=self.api_key,
                    node_id=self.node_id
                ).run(websocket)
            )

            # keep on processing commands from the server while possible
            while websocket.open:
                # cleanup pending_tasks
                pending_children = self.clean_pending_children(pending_children)

                # process the next request
                command_handler = await asyncio.ensure_future(self.process_command(websocket))
                if command_handler and isinstance(command_handler, ProcessWrapperCommand):
                    pending_children.append(command_handler)

        except Kill:
            # prevent orphans
            await WorkerManager.stop_all_children(pending_children)

            raise
        finally:
            if health_check_coroutine:
                logger.info("Stopping Health check")
                health_check_coroutine.cancel()

    async def run(self):

        reconnect = False # whether to try reconnecting with the same id

        # keep a connection to a websocket while we're alive
        while True:

            try:

                # connects to websocket on host
                async with websockets.connect(self.service_host) as websocket:
                    await self.register_and_process(websocket, reconnect)

            except Kill:
                logger.info("Shutting down node.")
                sys.exit(0)

            except WebsocketConnectionError:
                # print stack trace
                traceback.print_exc()

                self.num_reconnect_tries += 1
                logger.info("Error occured, sleeping before trying to reconnect")
                time.sleep(10)

            except:
                # print stack trace
                traceback.print_exc()

                raise

            finally:
                # If we have retried the max amount of times,
                # then stop trying to reconnect with the same id
                reconnect = self.num_reconnect_tries < MAX_RECONNECT_TRIES

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
        default=DEFAULT_SERVER,
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
