from command_handlers import *
from websocket_responses import *

response_to_command = {
    SpawnResponse: SpawnCommandHandler,
    ClientConnectedResponse: None,
    RegisterNodeResponse: None,
    ClientKillResponse: KillCommandHandler,
}
