from command_handlers.spawn_handler import SpawnCommandHandler
from command_handlers.kill_handler import KillCommandHandler
from command_handlers import response_to_command
import logging

logger = logging.getLogger("Command Handler Factory")
logger.setLevel(logging.DEBUG)

class CommandHandlerFactory():
    @staticmethod
    def get_handler(response):
        handler  = response_to_command.get(type(response), None)

        if handler is None:
            logger.warning("Could not recognize command %s", type(response))
            return None

        logger.debug("Got a %s command, using %s ", type(response), handler)

        return handler(response)
