import sys
import time
import os

# Optionally uses the environment variable UPPER to define an upper limit.
upper = os.environ.get('UPPER')
if upper:
    upper = int(upper)
else:
    upper = 10
print(upper)
for i in range(upper):
    sys.stdout.write('stdout #%d\n' %i)
    sys.stderr.write('stderr #%d\n' %i)
    time.sleep(1)

