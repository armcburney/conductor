import subprocess
import asyncio

import logging
import json

logger = logging.getLogger("Process Wrapper Command")
logger.setLevel(logging.DEBUG)

class NoRunningProcessException(Exception):
    pass

class ProcessWrapperCommand():
    """
    Command used to spawn a new process wrapper
    """
    def __init__(self, job_id, command, service_host, cwd=None, env=None):
        self.job_id = job_id
        self.command = command
        self.service_host = service_host
        self.cwd = cwd
        self.env = env
        self.process = None

    def __str__(self):
        return ' '.join(map(str, self.get_command()));

    def get_command(self):
        cmd = ['python3', 'process_wrapper.py',
                '--command', self.command,
                '--job_id', self.job_id,
                '--service_host', self.service_host]
        if self.cwd:
            cmd.extend(['--cwd', self.cwd])
        if self.env:
            cmd.extend(['--env', json.dumps(self.env)])
        return cmd

    async def launch_process_wrapper(self):
        process = await asyncio.create_subprocess_exec(
            *list(map(str, self.get_command())),
        )
        self.process = process
        return process

    async def kill_process(self):
        """
        Kills a process.
        """
        if self.process == None:
            raise NoRunningProcessException()

        self.process.send_signal(subprocess.signal.SIGKILL)

        # this should be instant
        await self.process.wait()


    async def stop_process(self):
        """
        Try to stop a process.
        """
        if self.process == None:
            raise NoRunningProcessException()

        self.process.send_signal(subprocess.signal.SIGTERM)

        # wait for the process to stop
        # await self.process.wait()

    async def wait(self):
        if self.done():
            return

        await self.process.wait()

    def done(self):
        if self.process == None:
            return True
        else:
            return self.process.returncode != None
