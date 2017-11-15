from websocket_responses import Response

class ClientConnectedResponse(Response):
    """
    client_connected command from server
    """
    def __init__(self, id, channel, user_id, success, result, token, server_token, **kwargs):
        self.node_id = id
        self.node_channel = channel
        self.user_id = user_id
        self.success = success
        self.result = result
        self.token = token
        self.server_token = server_token

    @classmethod
    def process_response(cls, response_body):
        return ClientConnectedResponse(**response_body[2])
