import json
from websocket_responses import *

class ResponseFactory():

    @classmethod
    def parse_response(cls, response):
        json_response = json.loads(response)

        command = json_response[0]

        response_type = None

        if command == "client_connected":
            response_type = ClientConnectedResponse
        elif command == "worker.registered":
            response_type = RegisterNodeResponse
        elif command == "worker.spawn":
            response_type = SpawnResponse
        elif command == "worker.connect":
            response_type = WorkerConnectedResponse
        elif command == "worker.delete":
            response_type = ClientKillResponse
        else:
            return None

        return response_type.process_response(json_response)
