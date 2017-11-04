from websocket_requests.command import Command

class RegisterNode(Command):
    def __init__(self, api_key, **kwargs):
        payload = {"key": api_key}
        payload.update(kwargs) # append any extra arguments
        super(RegisterNode, self).__init__(
            "worker.connect",
            payload
        )

