from test.mock_websocket import MockServer
from test.mock_websocket import WebsocketAction
from worker_master import WorkerManager, WebsocketConnectionError

import asyncio
import json
import unittest

def async_test(f):
    def wrapper(*args, **kwargs):
        coro = asyncio.coroutine(f)
        future = coro(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
    return wrapper

class TestWorkerMaster(unittest.TestCase):
    def setUp(self):
        self.mock_server = MockServer()

    def tearDown(self):
        self.mock_server = None

    @async_test
    async def test_pre_registration_success(self):
        self.mock_server.add_actions([
            WebsocketAction(lambda: '["client_connected",{"connection_id":"24bf41aa-0554-4966-bb01-c02c99ac9af1"},{"id":null,"channel":null,"user_id":null,"success":null,"result":null,"token":null,"server_token":null}]')
        ])

        websocket = self.mock_server.connect()

        await WorkerManager.pre_registration(websocket)

    @async_test
    async def test_pre_registration_fail(self):
        self.mock_server.add_actions([
            WebsocketAction(lambda: '["worker.connect",{"connection_id":"24bf41aa-0554-4966-bb01-c02c99ac9af1"},{"id":null,"channel":null,"user_id":null,"success":null,"result":null,"token":null,"server_token":null}]')
        ])

        websocket = self.mock_server.connect()

        # hack since there isnt support for assertions with coroutines
        try:
            await WorkerManager.pre_registration(websocket)
            self.assertTrue(False, 'This should have thrown a WebsocketConnectionError')
        except WebsocketConnectionError:
            pass

    @async_test
    async def test_registration(self):
        self.mock_server.add_actions([
            None, # get the initial connection request
            WebsocketAction(lambda: '["worker.connect",null,{"id":128540,"channel":null,"user_id":null,"success":true,"result":null,"token":null,"server_token":null}]'),
            WebsocketAction(lambda: '["worker.registered",{"id":10},{"id":null,"channel":null,"user_id":null,"success":null,"result":null,"token":null,"server_token":null}]')
        ])

        websocket = self.mock_server.connect()
        reconnect = False

        node_id = await WorkerManager.registration(websocket, api_key="test_api_key")
        self.assertEqual(node_id, 10)

        messages = websocket.get_messages()
        first_message = json.loads(messages[0])
        self.assertEqual(first_message[0], "worker.connect", 'Did not get the right type of message')
        self.assertEqual(first_message[1]['key'], "test_api_key", 'Did not receive the appropriate api key')


if __name__ == "__main__":
    unittest.main()
