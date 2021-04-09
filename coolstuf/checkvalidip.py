import ipaddress
from coolstuf import color as c


def check_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True, ip
    except ValueError:
        result = f'\n{c.C.RED}[✖]{c.C.END} Please enter a valid IPv4 address, {ip} is not valid!'
        return False, result
