#!/usr/bin/python3

import os
import threading
import time

class ServerHealth:
    pass

class HealthCheckThread(threading.Thread):

    def __init__(self, interval=10):
        self.interval = interval

    def get_server_health(self,):
        pass

    def send_stats(self, health):
        pass

    def run():
        while(True):
            self.send_stats(self.get_server_health())

            # sleep for some timeout
            time.sleep(self.interval)

class SlaveManager():

    def __init__(self):
        self._health_check_thread = threading.Thread()

        # start thread to send periodic health check
        self._health_check_thread.start()

    def spawn_worker_wrapper(self,):
        pass


if __name__ == "__main__":
    slave_manager = SlaveManager()
