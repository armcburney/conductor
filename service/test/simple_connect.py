from unittest import Mock
import unittest
from test.mock_websocket import MockServer


class TestConnection(unittest.TestCase):
    def setUp(self):
        self.mock_server = MockServer()

    def tearDown(self):
        self.mock_server = None

    def test_connect(self):
        self.mock_server.add_actions([
            WebsocketAction(lambda: '["client_connected",{"connection_id":"24bf41aa-0554-4966-bb01-c02c99ac9af1"},{"id":null,"channel":null,"user_id":null,"success":null,"result":null,"token":null,"server_token":null}]')
        ])
