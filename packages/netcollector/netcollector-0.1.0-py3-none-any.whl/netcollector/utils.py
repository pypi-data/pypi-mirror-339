from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException


NETMIKO_DEVICE_TYPES = {
    "cisco": "cisco_ios",
    "arista": "arista_eos",
    "cumulus": "linux",
}


def ssh_to_device(hostname, device_type, username, password):
    device_params = {
        'device_type': device_type,
        'host': hostname,
        'username': username,
        'password': password,
    }

    try:
        connection = ConnectHandler(**device_params)
        return connection
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        return None
