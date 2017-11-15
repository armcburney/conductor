from websocket_responses import Response

class SpawnResponse(Response):
    """
    worker.spawn
    """

    def __init__(self, id, script, working_directory, environment_variables, timeout, name, user_id, created_at, updated_at, **kwargs):
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
