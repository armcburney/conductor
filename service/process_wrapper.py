#!/usr/bin/python3
import os
import subprocess
import logging
import json
from subprocess import Popen
import asyncio
import signal
import sys

from argparse import ArgumentParser

import websockets
from websocket_adapter import RegisterJob, JobStdout, JobStdoutEof

logging.basicConfig()
logger = logging.getLogger("ProcessWrapper")
logger.setLevel(logging.DEBUG)

class ProcessWrapper():

    def __init__(self, api_key, service_host, job_id, command):
        self.api_key=api_key
        self.service_host=service_host
        self.job_id=job_id
        self.command=command

    async def start(self, loop):
        try:
            # connects to websocket on host
            async with websockets.connect(arguments.service_host) as websocket:
                register = RegisterJob({"job_id": arguments.job_id, "api_key": arguments.token})
                await websocket.send(str(register))
                logger.debug("Successfully connected to server.")

                logger.debug('Starting job: {}'.format(self.command))
                process = await asyncio.create_subprocess_exec(
                        *self.command.split(),
                        #stdin=asyncio.subprocess.PIPE,
                        stdout=asyncio.subprocess.PIPE)
                await asyncio.wait(
                    [
                        self.spawn_job(process, loop),
                        self.send_stdin(websocket, process.stdin),
                        self.read_stdout(websocket, process.stdout),
                    ],
                    loop=loop,
                    return_when=asyncio.ALL_COMPLETED)
        except Exception as e:
            logger.debug("Error occured, terminating:", e)


    # TODO investigate connecting pipes https://docs.python.org/3/library/asyncio-eventloop.html#connect-pipes
    # also https://docs.python.org/3/library/asyncio-eventloop.html#watch-file-descriptors
    async def send_stdin(self, websocket, writer):
        while websocket.open:
            msg = await websocket.recv()
            try:
                command, *payloads = json.loads(msg)
                logger.debug("Command: {} Payloads: {}".format(command, payloads))
                if command == 'stdin':
                    for payload in payloads:
                        writer.write(payload.encode())
                    await writer.drain()
                    continue
                if command == 'stdin.close':
                    writer.write_eof()
                    writer.close()
                    return
                logger.error("Unexpected websocket command: {}".format(command))
            except ValueError:
                logger.error("Failed to parse json: {}".format(msg))

    async def read_stdout(self, websocket, reader):
        while websocket.open:
            encoded = await reader.readline()
            if not encoded:
                return
            line = encoded.decode().strip()
            logger.debug("got stdout: {}".format(line))
            message = JobStdout(line)
            await websocket.send(str(message))
            logger.debug("sent message")

    async def spawn_job(self, process, loop):
        code = await process.wait()
        self._job_terminated(code)

    def ping_master(self):
        pass

    def _job_terminated(self, code):
        """
        Callback for when a job is finished
        """
        logger.debug('Terminated with code {}'.format(code))

    def _pre_word(self):
        """
        Code to setup a job
        """
        pass

if __name__ == "__main__":
    """
    Minimal implementation of spawn worker process.
    Runs a shell command and pipes stdin/stdout with a one character buffer.

    Example: printf 'foo\nbar' | python3 process_wrapper.py --job_id 1 --command 'cat'
    """
    parser = ArgumentParser("Worker job process wrapper.")

    parser.add_argument(
        "--token",
        dest="token",
        action="store",
        required=False,
        help="Provided api service token from Conductor."
    )

    parser.add_argument(
        "--service_host",
        dest="service_host",
        action="store",
        required=False,
        help="The service master to connect to.",
    )

    parser.add_argument(
        "--job_id",
        dest="job_id",
        action="store",
        required=True,
        help="The unique id for this worker job."
    )

    parser.add_argument(
        "--command",
        dest="command",
        action="store",
        required=True,
        help="The command to execute."
    )

    arguments = parser.parse_args()

    process_wrapper = ProcessWrapper(
        api_key=arguments.token,
        service_host=arguments.service_host,
        job_id=arguments.job_id,
        command=arguments.command,
    )
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(process_wrapper.start(loop))
        loop.run_forever()
    finally:
        loop.close()

