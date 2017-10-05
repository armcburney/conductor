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
        super(RegisterJob, self).__init__("new_job", None, *args)
