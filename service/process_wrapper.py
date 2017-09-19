#!/usr/bin/python3
import os
import subprocess
from subprocess import Popen

class ProcessWrapper():

    def __init__(self):
        pass

    def start(self):
        pass

    def spawn_job(self):
        pass

    def ping_master(self):
        pass

    def _job_terminated(self):
        """
        Callback for when a job is finished
        """
        pass

    def _pre_word(self):
        """
        Code to setup a job
        """
        pass

if __name__ == "__main__":
    process_wrapper = ProcessWrapper()
    process_wrapper.start()
