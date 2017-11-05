# Conductor Compute Node
The following module is a daemon to run locally on each host where you should be able to run commands. Multiple daemons can be spawned per host, though this shouldn't provide any benefit as most communication is done from individual jobs directly to the master server.

## Setup Host
First you need to install dependencies for the worker node. I recommend using a virtualenv to sandbox this python environment.

### Create sandboxed virtual environment (OPTIONAL)
```
virtualenv -p YOUR_PATH_TO_PYTHON3.6 .
. bin/activate # activate the virtualenv
```

### Install Requirements
```
pip install -r requirements.txt
```

## Provisioning
In order to provision a new node, start up `worker_master.py` with the provided api token. See `dev_scripts/test_live.sh` for an example.

```
python worker_master.py --service_host="ws://SERVICE_ADDRESS" --token="YOUR_API_TOKEN"
```

That it. You should now have a worker node capable of spawning jobs.
