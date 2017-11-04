from websocket_responses import Response

class RegisterNodeResponse(Response):
    """
    worker.registered
    """

    def __init__(self, id):
        self.node_id = id

    @classmethod
    def process_response(cls, response_body):
        return RegisterNodeResponse(**response_body[1])

