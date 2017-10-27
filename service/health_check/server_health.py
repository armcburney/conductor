import os

import psutil

class ServerHealth:
    """
    Encapsulate data pertaining to the current health of the server.
    """

    def __init__(
            self,
            cpu_count,
            load,
            total_memory,
            available_memory,
            total_disk,
            used_disk,
            free_disk
    ):
        self.cpu_count = cpu_count
        self.load = load
        self.total_memory = total_memory
        self.available_memory = available_memory
        self.total_disk = total_disk
        self.used_disk = used_disk
        self.free_disk = free_disk

    @staticmethod
    def create():
        """
        Create a new instance of a server healt object with current server stats.
        """

        cpu_count = psutil.cpu_count(logical=True)
        virtual_memory = psutil.virtual_memory()
        disk_usage = psutil.disk_usage("/")

        return ServerHealth(
            cpu_count=cpu_count,
            load=os.getloadavg(),
            total_memory=virtual_memory.total,
            available_memory=virtual_memory.available,
            total_disk=disk_usage.total,
            used_disk=disk_usage.used,
            free_disk=disk_usage.free,
        )

    def to_dict(self):
        """
        Convert the health status encapsulated in this object to a serializable dict
        """
        return {
            "cpu_count": self.cpu_count,
            "load": self.load[0],
            "total_memory": self.total_memory,
            "available_memory": self.available_memory,
            "total_disk": self.total_disk,
            "used_disk": self.used_disk,
            "free_disk": self.free_disk,
        }
