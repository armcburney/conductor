import websockets
import json

class WebsocketAdapter():
    """
    Adapter sitting translating logical server actions into websocket calls
    """

    @staticmethod
    async def register_channel(websocket, channel):
        await websocket.send("websocket_rails.subscribe")

    @staticmethod
    async def send_health(self):
        await websocket.send("device.event")

class Command:
    """
    Abstracted command so that we can represent operations in a more OO way
    """
    def __init__(self, cmd):
        self.cmd = cmd
        self.args = []

    def add_arg(self, arg_name, arg_value):
        self.args.append((arg_name, arg_value))

    def __str__(self):
        return json.dumps(self.__json__())

    def __json__(self):
        res = [self.cmd]
        for arg in self.args:
            res +=
        return res

class HealthCommand(Command):
    def __init__(self):
        super(Command, self).__init__("device.event")

class RegisterChannel(Command):
    def __init__(self):
        super(Command, self).__init__("websocket_rails.subscribe")
