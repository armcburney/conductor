from command_handlers.command_handler import CommandHandler

class SpawnCommandHandler(CommandHandler):
    def handle(self, command):

        # launch the job
        ProcessWrapperCommand(command.id, command.script, self.service_host).launch_process_wrapper()

