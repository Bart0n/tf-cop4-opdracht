from scapy.all import *


# Function returns 3 values. [0] is a nice formatted value for the CLI / Logging (result). [1] (port_state) can be
# used inside the program, a value of 0 means port closed, 1 means port open. [2] is what port number is scanned
def tcp_syn_scan(f_dst_ip, f_port, f_timeout, f_verbose):
    f_src_port = RandShort()
    f_tcp_syn_scan = sr1(IP(dst=f_dst_ip) / TCP(sport=f_src_port, dport=f_port, flags="S"), timeout=f_timeout, verbose=f_verbose)
    if str(type(f_tcp_syn_scan)) == "<class 'NoneType'>":
        result = f'[-] Port {f_port} closed'
        port_state = 0
        return result, port_state, f_port
    elif f_tcp_syn_scan.haslayer(TCP):
        if f_tcp_syn_scan.getlayer(TCP).flags == 0x12:
            sr(IP(dst=f_dst_ip) / TCP(sport=f_src_port, dport=f_port, flags="R"), timeout=f_timeout, verbose=f_verbose)
            result = f'[+] Port {f_port} open'
            port_state = 1
            return result, port_state, f_port
        elif f_tcp_syn_scan.getlayer(TCP).flags == 0x14:
            result = f'[-] Port {f_port} closed'
            port_state = 0
            return result, port_state, f_port
    else:
        return f'Something went completely wrong'
