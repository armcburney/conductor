import sys
import os
import time
import random

words = ['THINK', 'PAIR', 'SHARE']
seed = int(os.environ.get('SEED'))
iters = int(os.environ.get('ITERS'))

random.seed(seed)
time.sleep(1)

for _ in range(iters):
    sys.stdout.write('{} - {} - {}!\n'.format(
        random.choice(words), random.choice(words), random.choice(words)))
    time.sleep(0.5)

