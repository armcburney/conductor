from websocket_responses import Response

class ClientKillResponse(Response):
    """
    kill client
    """
    def __init__(self):
        pass

    @classmethod
    def process_response(cls, response_body):
        return ClientKillResponse()
