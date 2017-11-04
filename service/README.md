# Conductor Compute Node

## Setup
First you need to install dependencies for the worker node. I recommend using a virtualenv to sandbox this python environment.

### OPTIONAL
```
virtualenv -p YOUR_PATH_TO_PYTHON3.6 .
. bin/activate # activate the virtualenv
```

### Install Requirements
```
cd service
pip install -r requirements.txt
```

## Provisioning
In order to provision a new node, start up `worker_master.py` with the provided api token. See test_live for an example.

```
python worker_master.py --service_host="ws://SERVICE_ADDRESS" --token="YOUR_API_TOKEN"
```

## Test Server (Optional)
I've written a small test server to exercise basic functionality of the worker master. Run

```
python websocket_server_test.py
```

and then start the worker master pointing to this service. The script `dev_scripts/test_local.sh` is already setup to point to this mock socket server so alternatively you can just run that.
