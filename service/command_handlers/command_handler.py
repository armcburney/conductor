class CommandHandler():
    """
    ABC for a module to handle a specific command.
    """
    def __init__(self, command):
        self.command = command

    async def handle(self, **kwargs):
        pass
