from websocket_responses import *

object_mappings = {
    "client_connected" : ClientConnectedResponse,
    "worker.registered": RegisterNodeResponse,
    "worker.spawn": SpawnResponse,
    "worker.connect": WorkerConnectedResponse,
    "worker.delete": ClientKillResponse,
}
