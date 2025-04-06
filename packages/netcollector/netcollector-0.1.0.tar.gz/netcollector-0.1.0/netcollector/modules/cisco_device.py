import re
import socket
import time
from netcollector.base_device import BaseDevice

class CiscoDevice(BaseDevice):
    def __init__(self, ssh_connection):
        self.connection = ssh_connection

    def get_ntp(self):
        self.connection.send_command("terminal length 0", expect_string="#")
        time.sleep(0.2)
        self.connection.clear_buffer()

        # Run ntp config
        ntp_config = self.connection.send_command("show run | i ntp", expect_string="#")
        time.sleep(0.3)

        # Try preferred command
        self.connection.clear_buffer()
        ntp_status = self.connection.send_command("show ntp peer-status", expect_string="#")
        time.sleep(0.3)

        # Fallback to associations if peer-status fails or returns no usable data
        if not ntp_status.strip() or "remote" not in ntp_status.lower():
            print("Fallback: using 'show ntp associations'")
            self.connection.clear_buffer()
            ntp_status = self.connection.send_command("show ntp associations", expect_string="#")
            time.sleep(0.3)

        result = {
            "vendor": "cisco",
            "ntp_servers": [],
            "source_interface": None,
        }

        # Extract source-interface
        match_src = re.search(r"ntp source-interface\s+(\S+)", ntp_config)
        if match_src:
            result["source_interface"] = match_src.group(1)

        # Get list of servers from config
        ntp_servers = re.findall(r"ntp server\s+(\d+\.\d+\.\d+\.\d+)", ntp_config)

        for server_ip in ntp_servers:
            sync_state = "not selected"

            for line in ntp_status.splitlines():
                if server_ip in line:
                    # Handle both styles: peer-status (*) and associations (*~)
                    if line.strip().startswith("*") or "*~" in line:
                        sync_state = "selected"
                    break

            try:
                dns_name = socket.gethostbyaddr(server_ip)[0]
            except socket.herror:
                dns_name = None

            result["ntp_servers"].append({
                "ip": server_ip,
                "dns": dns_name,
                "sync_state": sync_state
            })

        return result

    def disconnect(self):
        self.connection.disconnect()
