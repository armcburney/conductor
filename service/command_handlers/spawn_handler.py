from command_handlers.command_handler import CommandHandler
from process_wrapper_command import ProcessWrapperCommand

class SpawnCommandHandler(CommandHandler):
    async def handle(self, **kwargs):
        """
            command: the SpawnCommand to attempt to spawn

            Return:
                The process wrapper command instance so we can control this job.
        """

        command = self.command

        # launch the job
        wrapper = ProcessWrapperCommand(
            command.id,
            command.script,
            kwargs["service_host"]
        )

        process = await wrapper.launch_process_wrapper()

        return wrapper
