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
from websocket_requests.job_commands import JobStdout, JobStderr, JobReturnCode

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('ProcessWrapper')
logger.setLevel(logging.DEBUG)

class WebsocketConnection():

    def __init__(self, service_host, q):
        self.q = q
        self.service_host = service_host

    async def run(self):
        reconnect_count = 0
        while True:
            try:
                async with websockets.connect(self.service_host) as websocket:
                    reconnect_count = 0
                    while websocket.open:
                        msg = await self.q.get()
                        if msg is None:
                            return
                        await websocket.send(msg)
                        self.q.task_done()
            except websockets.exceptions.ConnectionClosed as e:
                if reconnect_count >= 10:
                    # Failed to reconnect 10 times, abort.
                    logger.critical('Failed to establish websocket connection, aborting.')
                    raise e
                logger.debug('sleeping before reconnecting websocket...')
                await asyncio.sleep(0.1 * (1 << reconnect_count)) # Exponential backoff
                reconnect_count += 1

class ProcessWrapper():

    def __init__(self, api_key, service_host, job_id, command, cwd='', env=None):
        self.api_key=api_key
        self.service_host=service_host
        self.job_id=job_id
        self.command=command
        self.cwd=cwd
        self.env=env

    async def start(self, loop):
        q = asyncio.Queue(1, loop=loop)
        websocket = WebsocketConnection(self.service_host, q)
        asyncio.ensure_future(websocket.run(), loop=loop)
        try:
            # connects to websocket on host
            async with websockets.connect(self.service_host) as websocket:
                logger.debug('Successfully connected to server.')

                logger.info('Starting job: {}'.format(self.command))
                process = await asyncio.create_subprocess_shell(
                        self.command,
                        #stdin=asyncio.subprocess.PIPE,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        cwd=self.cwd if self.cwd != '' else None,
                        env=self.env)
                await asyncio.wait(
                    [
                        self.spawn_job(process, loop, q),
                        #self.send_stdin(websocket, process.stdin),
                        self.read_stdout(q, process.stdout),
                        self.read_stderr(q, process.stderr),
                    ],
                    loop=loop,
                    return_when=asyncio.ALL_COMPLETED)
                await q.put(None) # Stop WebsocketConnection.
                await asyncio.sleep(0.5)
                logger.debug('Returned from await job')
        except Exception as e:
            logger.debug('Error occured, terminating:', e)

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

    async def read_stdout(self, q, reader):
        encoder = lambda msg: JobStdout(msg, key=self.api_key, id=self.job_id)
        await self._queue_writer(q, reader, encoder)

    async def read_stderr(self, q, reader):
        encoder = lambda msg: JobStderr(msg, key=self.api_key, id=self.job_id)
        await self._queue_writer(q, reader, encoder)

    async def _queue_writer(self, q, reader, encoder):
        while True:
            encoded = await reader.readline()
            if not encoded:
                logger.debug('sending eof')
                await q.put(str(encoder('')))
                return
            line = encoded.decode()
            await q.put(str(encoder(line)))

    async def spawn_job(self, process, loop, q):
        code = await process.wait()
        logger.debug('Terminated with code {}'.format(code))
        await q.put(str(JobReturnCode(code, key=self.api_key, id=self.job_id)))
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

    parser.add_argument(
        '--cwd',
        dest='cwd',
        action='store',
        required=False,
        help='Working directory in which to execute the command.'
    )

    parser.add_argument(
        '--env',
        dest='env',
        action='store',
        required=False,
        help='Modify the environment in which the command is executed.'
    )

    arguments = parser.parse_args()

    process_wrapper = ProcessWrapper(
        api_key=arguments.token,
        service_host=arguments.service_host,
        job_id=arguments.job_id,
        command=arguments.command,
        cwd=arguments.cwd,
        env=json.loads(arguments.env) if arguments.env else None,
    )
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(process_wrapper.start(loop))
    finally:
        loop.close()

