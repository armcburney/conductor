from command_handlers.spawn_handler import SpawnCommandHandler
from websocket_responses import SpawnResponse, ClientConnectedResponse, RegisterNodeResponse
import logging

logging.basicConfig()
logger = logging.getLogger("Command Handler Factory")
logger.setLevel(logging.DEBUG)

class CommandHandlerFactory():
    @staticmethod
    def get_handler(response):
        handler  = None
        if type(response) is SpawnResponse:
            # spawn a job
            logger.info("Got a spawn command")
            handler = SpawnCommandHandler

        elif type(response) is ClientConnectedResponse:
            logger.debug("Got a Connect command")
            #TODO: add handler

        elif type(response) is RegisterNodeResponse:
            logger.debug("Got a Register command")
            #TODO: add handler

        else:
            logger.debug("Could not recognize command.")

        if handler is None:
            return None

        return handler(response)
