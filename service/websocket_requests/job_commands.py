from websocket_requests.command import Command

class JobStdout(Command):
    def __init__(self, stdout, **kwargs):
        super(JobStdout, self).__init__('job.stdout', {'stdout': stdout, **kwargs})

class JobStderr(Command):
    def __init__(self, stderr, **kwargs):
        super(JobStderr, self).__init__('job.stderr', {'stderr': stderr, **kwargs})

class JobReturnCode(Command):
    def __init__(self, code, **kwargs):
        super(JobReturnCode, self).__init__('job.return_code', {'return_code': code, **kwargs})
