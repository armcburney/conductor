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
from websocket_requests import JobStdout, JobStderr, JobReturnCode

logging.basicConfig()
logger = logging.getLogger('ProcessWrapper')
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
                logger.debug('Successfully connected to server.')

                logger.debug('Starting job: {}'.format(self.command))
                process = await asyncio.create_subprocess_shell(
                        self.command,
                        #stdin=asyncio.subprocess.PIPE,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE)
                await asyncio.wait(
                    [
                        self.spawn_job(process, loop, websocket),
                        #self.send_stdin(websocket, process.stdin),
                        self.read_stdout(websocket, process.stdout),
                        self.read_stderr(websocket, process.stderr),
                    ],
                    loop=loop,
                    return_when=asyncio.ALL_COMPLETED)
                await asyncio.sleep(0.5) # Dirty hack - TODO wait for websocket to flush before closing it
                logger.debug('Returned from await job')
        except Exception as e:
            logger.debug('Error occured, terminating:', e)


    # TODO investigate connecting pipes https://docs.python.org/3/library/asyncio-eventloop.html#connect-pipes
    # also https://docs.python.org/3/library/asyncio-eventloop.html#watch-file-descriptors
    async def send_stdin(self, websocket, writer):
        while websocket.open:
            msg = await websocket.recv()
            try:
                command, *payloads = json.loads(msg)
                logger.debug('Command: {} Payloads: {}'.format(command, payloads))
                if command == 'job.stdin':
                    for payload in payloads:
                        writer.write(payload.encode())
                    await writer.drain()
                    continue
                if command == 'job.stdin_close':
                    writer.write_eof()
                    writer.close()
                    return
                logger.error('Unexpected websocket command: {}'.format(command))
            except ValueError:
                logger.error('Failed to parse json: {}'.format(msg))

    async def read_stdout(self, websocket, reader):
        encoder = lambda msg: JobStdout(msg, key=self.api_key, id=self.job_id)
        await self._websocket_writer(websocket, reader, encoder)

    async def read_stderr(self, websocket, reader):
        encoder = lambda msg: JobStderr(msg, key=self.api_key, id=self.job_id)
        await self._websocket_writer(websocket, reader, encoder)

    async def _websocket_writer(self, websocket, reader, encoder):
        while websocket.open:
            encoded = await reader.readline()
            if not encoded:
                logger.debug('sending eof')
                await websocket.send(str(encoder('')))
                return
            line = encoded.decode()
            await websocket.send(str(encoder(line)))
            logger.debug('sent message: "{}"'.format(line))

    async def spawn_job(self, process, loop, websocket):
        code = await process.wait()
        logger.debug('Terminated with code {}'.format(code))
        await websocket.send(str(JobReturnCode(code, key=self.api_key, id=self.job_id)))
        logger.debug('Sent job return code')

    def ping_master(self):
        pass


if __name__ == '__main__':
    '''
    Minimal implementation of spawn worker process.
    Runs a shell command and pipes stout/stderr line by line to websocket host.

    Example:  python3 process_wrapper.py --job_id 1 --command '/usr/bin/python3 -u write_test.py' --service_host ws://localhost:8765
    '''
    parser = ArgumentParser('Worker job process wrapper.')

    parser.add_argument(
        '--token',
        dest='token',
        action='store',
        required=False,
        help='Provided api service token from Conductor.'
    )

    parser.add_argument(
        '--service_host',
        dest='service_host',
        action='store',
        required=False,
        help='The service master to connect to.',
    )

    parser.add_argument(
        '--job_id',
        dest='job_id',
        action='store',
        required=True,
        help='The unique id for this worker job.'
    )

    parser.add_argument(
        '--command',
        dest='command',
        action='store',
        required=True,
        help='The command to execute.'
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
    finally:
        loop.close()

