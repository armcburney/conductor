import subprocess
import asyncio

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
        return 'python3 process_wrapper.py --command="{0}" --job_id={1} --service_host="{2}"'.format(self.command, self.job_id, self.service_host)

    def get_command(self):
        return ['python3', 'process_wrapper.py',
                '--command', self.command,
                '--job_id', self.job_id,
                '--service_host', self.service_host]

    async def launch_process_wrapper(self):
        process = await asyncio.create_subprocess_exec(
            self.get_command(),
            cwd=self.cwd if self.cwd != "" else None,
            env=self.env
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
        # TODO: make sure this doesnt stop our event loop indefinitely
        await self.process.wait()


