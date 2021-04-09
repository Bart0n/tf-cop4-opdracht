from scapy.all import *


# Function returns 3 values. [0] is a nice formatted value for the CLI / Logging (result). [1] (port_state) can be
# used inside the program, a value of 0 means port closed, 1 means port open. [2] is what port number is scanned
def udp_scan(f_dst_ip, f_port, f_timeout, f_verbose):
    f_src_port = RandShort()
    f_udp_scan = sr1(IP(dst=f_dst_ip)/UDP(sport= f_src_port, dport=f_port), timeout=f_timeout, verbose=f_verbose)
    if str(type(f_udp_scan)) == "<class 'NoneType'>":
        result = f'[+] Port {f_port} open or filtered'
        port_state = 1
        return result, port_state, f_port

    elif f_udp_scan.haslayer(UDP):
        result = f'[+] Port {f_port} open'
        port_state = 1
        return result, port_state, f_port
    elif f_udp_scan.haslayer(ICMP):
        if int(f_udp_scan.getlayer(ICMP).type) == 3 and int(f_udp_scan.getlayer(ICMP).code) == 3:
            result = f'[-] Port {f_port} closed'
            port_state = 0
            return result, port_state, f_port
        elif int(f_udp_scan.getlayer(ICMP).type) == 3 and int(f_udp_scan.getlayer(ICMP).code) in [1, 2, 9, 10, 13]:
            result = f'[-] Port {f_port} filtered'
            port_state = 0
            return result, port_state, f_port

    else:
        return f'Something went completely wrong'
