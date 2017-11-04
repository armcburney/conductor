import time
import sys
import signal

sys.stdout.write("starting\n")

def term_handler(signum, frame):
    sys.stdout.write("I dont wanna DIE. You cant kill me.\n")

signal.signal(signal.SIGTERM, term_handler)

while True:
    sys.stdout.write("Life is sad\n")
    sys.stdout.flush()
    time.sleep(1)
