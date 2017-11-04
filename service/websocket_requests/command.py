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

