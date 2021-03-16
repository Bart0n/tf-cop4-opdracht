from scapy.all import *
from coolstuf import database
from coolstuf import log_handler
from datetime import date


def tcp_connect_scan(f_dst_ip, f_log, f_port, f_timeout, f_verbose, f_show_closed, f_db):
    all_result = []
    for i in f_port:
        i = int(i)
        f_src_port = RandShort()
        f_tcp_connect_scan = sr1(IP(dst=f_dst_ip) / TCP(sport=f_src_port,
                                                        dport=i, flags="S"), timeout=f_timeout, verbose=f_verbose)
        if str(type(f_tcp_connect_scan)) == "<class 'NoneType'>":
            result = f'[-] Port {i} closed'
            all_result += [result]
            if f_show_closed:
                print(result)
        elif f_tcp_connect_scan.haslayer(TCP):
            if f_tcp_connect_scan.getlayer(TCP).flags == 0x12:
                f_send_reset = sr(IP(dst=f_dst_ip) / TCP(sport=f_src_port,
                                                         dport=i, flags="RA"), timeout=f_timeout, verbose=f_verbose)
                result = f'[+] Port {i} open'
                all_result += [result]
                print(result)
            elif tcp_connect_scan.getlayer(TCP).flags == 0x14:
                result = f'[-] Port {i} closed'
                all_result += [result]
                if f_show_closed:
                    print(result)
        else:
            print(f'Something went completely wrong')
    data_for_db = (date.today().strftime("%d/%m/%Y"), f_dst_ip, 'tcp-connect', str(f_port), str(all_result))
    database.insert_data(f_db, data_for_db)
    log_handler.write_output(f_dst_ip, 'tcp-connect', f_port, f_timeout, all_result, f_log[1], f_log[0])

