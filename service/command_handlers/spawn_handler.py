from command_handlers.command_handler import CommandHandler

class SpawnCommandHandler(CommandHandler):
    def handle(self, command):
        """
            command: the SpawnCommand to attempt to spawn

            Return:
                The process wrapper command instance so we can control this job.
        """

        # launch the job
        return ProcessWrapperCommand(command.id, command.script, self.service_host).launch_process_wrapper()

