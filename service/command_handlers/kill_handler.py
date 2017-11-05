from command_handlers.command_handler import CommandHandler
from global_commands import Kill
import signal
import sys

class KillCommandHandler(CommandHandler):
    async def handle(self, **kwargs):

        # send this message to upstream caller
        raise Kill()
