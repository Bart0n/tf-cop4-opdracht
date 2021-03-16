import ipaddress


def check_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        print(f'Please enter a valid IPv4 address, {ip} is not valid!')
        return False
