from netcollector.base_device import BaseDevice

class AristaDevice(BaseDevice):
    def __init__(self, ssh_connection):
        self.connection = ssh_connection

    def get_bgp(self):
        output = self.connection.send_command("show ip bgp summary")
        return {"vendor": "arista", "bgp": output}

    def get_ntp(self):
        output = self.connection.send_command("show ntp status")
        return {"vendor": "arista", "ntp": output}

    def disconnect(self):
        self.connection.disconnect()