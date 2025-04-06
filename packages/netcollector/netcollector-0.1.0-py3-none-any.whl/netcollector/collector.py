from netcollector.modules.cisco_device import CiscoDevice
from netcollector.modules.arista_device import AristaDevice
from netcollector.modules.cumulus_device import CumulusDevice
from netcollector.utils import ssh_to_device

DEVICE_MAP = {
    "cisco": CiscoDevice,
    "arista": AristaDevice,
    "cumulus": CumulusDevice,
}

NETMIKO_DEVICE_TYPES = {
    "cisco": "cisco_ios",
    "arista": "arista_eos",
    "cumulus": "linux",
}

class Collector:
    def __init__(self, vendor, host, username, password):
        if vendor not in DEVICE_MAP:
            raise ValueError(f"Unsupported vendor: {vendor}")

        netmiko_type = NETMIKO_DEVICE_TYPES.get(vendor)
        if not netmiko_type:
            raise ValueError(f"Missing Netmiko device_type for vendor: {vendor}")

        self.connection = ssh_to_device(
            hostname=host,
            device_type=netmiko_type,
            username=username,
            password=password
        )

        if not self.connection:
            raise Exception("SSH connection failed")

        self.device = DEVICE_MAP[vendor](self.connection)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def collect(self, params):
        data = {}
        for param in params:
            func = getattr(self.device, f"get_{param}", None)
            if callable(func):
                data[param] = func()
            else:
                data[param] = {"error": f"{param} not supported"}
        return data

    def disconnect(self):
        self.device.disconnect()
