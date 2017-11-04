from command_handlers.command_handler import CommandHandler
from process_wrapper_command import ProcessWrapperCommand

class SpawnCommandHandler(CommandHandler):
    async def handle(self, **kwargs):
        """
            self.command: the SpawnCommand to attempt to spawn

            Return:
                The process wrapper command instance so we can control this job.
        """

        command = self.command

        # launch the job
        wrapper = ProcessWrapperCommand(
            command.id,
            command.script,
            service_host=kwargs["service_host"],
            cwd=command.working_directory,
            env=command.environment_variables,
        )

        process = await wrapper.launch_process_wrapper()

        return wrapper
