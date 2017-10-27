from command_handlers.command_handler import CommandHandler
import signal

class KillCommandHandler(CommandHandler):
    async def handle(self, **kwargs):
        """
            command: the KillCommand to attempt to spawn

            Return:
                True if the command is correct
        """

        # dummy class just so we can follow a consistent standard
        sys.exit(0)
