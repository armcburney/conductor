import websockets
import json

class Command:
    """
    Abstracted command so that we can represent operations in a more OO way
    """
    def __init__(self, cmd, *args):
        self.cmd = cmd
        self.args = args

    def add_arg(self, arg_name, arg_value):
        self.args.append((arg_name, arg_value))

    def __str__(self):
        return json.dumps(self.__json__())

    def __json__(self):
        res = [self.cmd]
        for arg in self.args:
            res.append(arg)
        return res

class HealthCommand(Command):
    def __init__(self, *args):
        super(HealthCommand, self).__init__("health_check", *args)

class RegisterNode(Command):
    def __init__(self, *args):
        super(RegisterNode, self).__init__("connect", None, *args)

class RegisterJob(Command):
    def __init__(self, *args):
        super(RegisterJob, self).__init__('worker.register_job', *args)

class JobStdin(Command):
    def __init__(self, *args):
        super(JobStdin, self).__init__('stdin', *args)

class JobStdout(Command):
    def __init__(self, *args):
        super(JobStdout, self).__init__('stdout', *args)

class JobStdoutEof(Command):
    def __init__(self, *args):
        super(JobStdoutEof, self).__init__('stdout.eof', *args)

class JobStderr(Command):
    def __init__(self, *args):
        super(JobStderr, self).__init__('stderr', *args)

class JobStderrEof(Command):
    def __init__(self, *args):
        super(JobStderrEof, self).__init__('stderr.eof', *args)
