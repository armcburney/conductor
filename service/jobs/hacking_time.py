import time
import uuid
import os

print ("Turning up new Nodes:{}".format([str(uuid.uuid4()) for x in range(10)]))
time.sleep(5)

print ("Starting MONGODB Database migration")

if os.environ.get('OOM', False):
    raise Exception("Some Exception")

TOTAL = 101
for i in range(TOTAL):
    print  ("Migrating shard {}. Migration {:.03}% complete".format(uuid.uuid4(), float(i)/TOTAL * 100))
    time.sleep(0.5)

print ("Migration SUCCEEDED. Unfortunately, you're still using mongo")


