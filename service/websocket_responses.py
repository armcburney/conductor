import json
class ResponseNotSupportedException(Exception):
    pass

class ResponseFactory():

    @classmethod
    def parse_response(cls, response):
        json_response = json.loads(response)
        command = json_response[0]

        response_type = None

        if command == "worker.connect":
            response_type = ConnectNodeResponse
        elif command == "worker.registered":
            response_type = RegisterNodeResponse
        elif command == "spawn":
            response_type = SpawnResponse
        else:
            raise ResponseNotSupportedException

        return response_type.process_response(json_response)


class Response():
    @staticmethod
    def process_response(response_body):
        raise NotImplementedError

class RegisterNodeResponse(Response):
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
        return RegisterNodeResponse(**response_body)

class ConnectNodeResponse(Response):
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
        return ConnectNodeResponse(**response_body[2])

class SpawnResponse(Response):

    def __init__(self, id, script, working_directory, environment_variables, timeout, name, user_id, created_at, updated_at):
        self.id = id
        self.script = script
        self.working_directory = working_directory
        self.environment_variables = environment_variables
        self.timeout = timeout
        self.name = name
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def process_response(cls, response_body):
        return SpawnResponse(**response_body[1])
