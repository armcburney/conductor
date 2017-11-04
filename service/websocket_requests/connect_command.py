from websocket_requests.register_node import RegisterNode

class ConnectCommand(RegisterNode):
    def __init__(self, api_key, node_id, **kwargs):
        super(ConnectCommand, self).__init__(
            api_key=api_key,
            node_id=node_id,
            **kwargs
        )
