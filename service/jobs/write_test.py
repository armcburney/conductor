import sys
import time

for i in range(10):
    sys.stdout.write('stdout #%d\n' %i)
    sys.stderr.write('stderr #%d\n' %i)
    time.sleep(0.5)

