#!/usr/bin/python3
import os
import subprocess
import logging
from subprocess import Popen
import asyncio
import signal
import sys

from argparse import ArgumentParser

logging.basicConfig()
logger = logging.getLogger("ProcessWrapper")
logger.setLevel(logging.DEBUG)

class ProcessWrapper():

    def __init__(self, api_key, service_host, job_id, command):
        self.api_key=api_key
        self.service_host=service_host
        self.job_id=job_id
        self.command=command

    async def start(self, loop, websocket):
        logger.debug('Starting job: {}'.format(self.command))
        process = await asyncio.create_subprocess_shell(
                self.command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE)
        job = asyncio.ensure_future(self.spawn_job(process, loop))
        writer = asyncio.ensure_future(self.send_stdin(process.stdin))
        reader = asyncio.ensure_future(self.read_stdout(process.stdout))

    # TODO investigate connecting pipes https://docs.python.org/3/library/asyncio-eventloop.html#connect-pipes
    # also https://docs.python.org/3/library/asyncio-eventloop.html#watch-file-descriptors
    async def send_stdin(self, writer):
        # TODO hook up to web socket
        while 1:
            ch = sys.stdin.read(1)
            if not ch:
                writer.close()
                return
            writer.write(ch.encode())

    async def read_stdout(self, reader):
        # TODO hook up to web socket
        while 1:
            ch = await reader.read(1)
            if not ch: return
            sys.stdout.write(ch.decode())

    async def spawn_job(self, process, loop):
        code = await process.wait()
        self._job_terminated(code)
        loop.stop()

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
        # connects to websocket on host
        async with websockets.connect(arguments.service_host) as websocket:

            # register this node with the main server
            logger.debug("Initiating websocket connection with", arguments.service_host)
            await self.initiate_connection(websocket)

            # schedule the reporter coroutine
            self.health_check_coroutine = asyncio.ensure_future(HealthCheckCoroutine().run(websocket))

            # keep on processing commands while possible
            while websocket.open:
                await asyncio.ensure_future(self.process_command(websocket))

        logger.debug("ProcessWrapper {} dead".format(job_id))
        loop.run_until_complete(process_wrapper.start(loop=loop))
        loop.run_forever()
    except:
        logger.debug("Error occured, terminating.")
    finally:
        loop.close()

