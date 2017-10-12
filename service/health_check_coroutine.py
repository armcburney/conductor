import logging
import asyncio

from server_health import ServerHealth
from websocket_requests import HealthCommand

class HealthCheckCoroutine():
    """
    Periodically poll the system and send stats to the master.
    """

    def __init__(self, interval=10, logger=logging.getLogger()):
        self.interval = interval
        self.logger = logger


    @staticmethod
    def get_server_health():
        return ServerHealth.create()

    async def send_stats(self, websocket):
        health = HealthCommand(self.get_server_health().to_dict())
        self.logger.debug("Sending Server Health Status")
        self.logger.debug(str(health))
        await websocket.send(str(health))
        self.logger.debug("Sent Server Health Status")


    async def run(self, websocket):
        self.logger.debug("Starting health check coroutine.")

        # keep sending stats forever
        while websocket.open:

            await self.send_stats(websocket)

            # sleep for some timeout
            await asyncio.sleep(self.interval)

