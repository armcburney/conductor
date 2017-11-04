import sys
import os
import time

for key in sys.argv[1:]:
    val = os.environ.get(key)
    sys.stdout.write('env variable "{}"={}\n'.format(key, val))

