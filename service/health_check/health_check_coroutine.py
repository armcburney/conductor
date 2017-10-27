import logging
import asyncio

from health_check.server_health import ServerHealth
from websocket_requests import HealthCommand

class HealthCheckCoroutine():
    """
    Periodically poll the system and send stats to the master.
    """

    def __init__(self, api_key, node_id, interval=10, logger=logging.getLogger()):
        self.interval = interval
        self.logger = logger
        self.api_key = api_key
        self.node_id = node_id

    @staticmethod
    def get_server_health():
        return ServerHealth.create()

    async def send_stats(self, websocket):

        health = HealthCommand(self.get_server_health().to_dict(), api_key=self.api_key, id=self.node_id)
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

