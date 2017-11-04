from websocket_responses import Response

class WorkerConnectedResponse(Response):
    """
    worker.connect
    """

    def __init__(self, id, channel, user_id, success, result, token, server_token):
        self.node_id = id
        self.node_channel = channel
        self.user_id = user_id
        self.success = success
        self.result = result
        self.token = token
        self.server_token = server_token

    @classmethod
    def process_response(cls, response_body):
        return WorkerConnectedResponse(**response_body[2])


