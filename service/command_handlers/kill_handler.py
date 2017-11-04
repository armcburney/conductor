from command_handlers.command_handler import CommandHandler
from global_commands import Kill
import signal
import sys

class KillCommandHandler(CommandHandler):
    async def handle(self, **kwargs):
        # dummy class just so we can follow a consistent standard
        raise Kill()
