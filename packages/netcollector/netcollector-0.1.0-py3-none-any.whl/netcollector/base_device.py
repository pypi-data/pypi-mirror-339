from abc import ABC, abstractmethod

class BaseDevice(ABC):
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    @abstractmethod
    def get_ntp(self):
        pass
