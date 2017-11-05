from websocket_requests.command import Command

class HealthCommand(Command):
    def __init__(self, health_dict, api_key, id):
        temp_dict = health_dict
        temp_dict.update({"key": api_key})
        temp_dict.update({"id": id})
        super(HealthCommand, self).__init__("worker.healthcheck", temp_dict)

