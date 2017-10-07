# Conductor Compute Node

## Provisioning
In order to provision a new node, start up `slave_master.py` with the provided api token.

```
python slave_master.py --hostname="YOUR_IDENTIFICATION_HERE" --service_host="ws://SERVICE_ADDRESS" --token="YOUR_API_TOKEN"
```

## Test Server
I've written a small test server to exercise basic functionality of the slave master. Run

```
python websocket_server_test.py
```

and then start the slave master pointing to this service. The script `test_local.sh` is already setup to point to this mock socket server so alternatively you can just run that.
