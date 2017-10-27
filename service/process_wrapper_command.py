import asyncio

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
        return process
