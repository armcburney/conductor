class MockWebsocket:
    def __init__(self, actions=[]):
        # holds the actions the server should enact
        # Each response is a lambda that generates a string
        # None means wait for user command
        self.actions = actions

    def add_action(self, action):
        self.actions.append(action)

    async def send(self):
        assert (self.actions[0] is None)
        self.actions.pop(0)

    async def recv(self):
        func = self.actions[0]
        self.actions.pop(0)
        return func()

class MockServer:
    def __init__(self):
        self.websocket = MockWebsocket()

    def add_action(self, action):
        self.websocket.add_action(action)

    def add_actions(self, actions):
        for action in actions:
            self.websocket.add_action(action)

    def connect(self):
        return self.websocket

class WebsocketAction:
    def __init__(self, data):
        self.data = data

    def __call__(self):
        self.data()
