import websockets
import json

class Command:
    """
    Abstracted command so that we can represent operations in a more OO way.
    Each argument is an element in the tuple being sent over the wire to the main master.
    """

    def __init__(self, cmd, *args):
        self.cmd = cmd
        self.args = args

    def add_arg(self, arg_name, arg_value):
        self.args.append((arg_name, arg_value))

    def __str__(self):
        return json.dumps(self.__getjson__())

    def __getjson__(self):
        res = [self.cmd]
        for arg in self.args:
            res.append(arg)
        return res

class HealthCommand(Command):
    def __init__(self, health_dict):
        super(HealthCommand, self).__init__("health_check", health_dict)

class RegisterNode(Command):
    def __init__(self, api_key, **kwargs):
        payload = {"key": api_key}
        payload.update(kwargs) # append any extra arguments
        super(RegisterNode, self).__init__(
            "worker.connect",
            payload
        )

class JobStdout(Command):
    def __init__(self, *args):
        super(JobStdout, self).__init__('job.stdout', {{'stdout': stdout, **kwargs})

class JobStderr(Command):
    def __init__(self, stderr, **kwargs):
        super(JobStderr, self).__init__('job.stderr', {{'stderr': stderr, **kwargs})

class JobReturnCode(Command):
    def __init__(self, code, **kwargs):
        super(JobReturnCode, self).__init__('job.return_code', {'code': code, **kwargs})

class ConnectCommand(RegisterNode):
    def __init__(self, api_key, node_id, **kwargs):
        super(ConnectCommand, self).__init__(
            api_key=api_key,
            node_id=node_id,
            **kwargs
        )
