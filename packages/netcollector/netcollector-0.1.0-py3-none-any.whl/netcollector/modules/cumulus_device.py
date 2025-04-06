from netcollector.base_device import BaseDevice

class CumulusDevice(BaseDevice):
    def __init__(self, ssh_connection):
        self.connection = ssh_connection

    def get_ntp(self):
        output = self.connection.send_command("ntpq -p")
        return {"vendor": "cumulus", "ntp": output}

    def disconnect(self):
        self.connection.disconnect()