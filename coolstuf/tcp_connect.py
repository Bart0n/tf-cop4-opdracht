import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


def tcp_connect_scan(f_dst_ip, f_log, f_port, f_timeout, f_verbose):
    f_src_port = RandShort()
    f_tcp_connect_scan = sr1(IP(dst=f_dst_ip) / TCP(sport=f_src_port,
                                                    dport=f_port, flags="S"), timeout=f_timeout, verbose=f_verbose)
    if str(type(f_tcp_connect_scan)) == "<class 'NoneType'>":
        result = f'Port {f_port} closed'
        print(result)
        return result
    elif f_tcp_connect_scan.haslayer(TCP):
        if f_tcp_connect_scan.getlayer(TCP).flags == 0x12:
            f_send_reset = sr(IP(dst=f_dst_ip) / TCP(sport=f_src_port,
                                                     dport=f_port, flags="RA"), timeout=f_timeout, verbose=f_verbose)
            result = f'Port {f_port} open'
            print(result)
            return result
        elif tcp_connect_scan.getlayer(TCP).flags == 0x14:
            result = f'Port {f_port} closed'
            print(result)
            return result