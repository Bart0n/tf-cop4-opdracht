from coolstuf import color as c


def port_format(port):
    dst_port = []
    port = port.lower()
    contain_letters = port.islower()
    if not contain_letters:
        if "-" in port:
            pl = port.split("-")
            pl = [int(x) for x in pl]
            pl.sort()
            pl_low = int(pl[0])
            pl_high = int(pl[1]) + 1
            pl = range(pl_low, pl_high, 1)
            dst_port += pl
            return dst_port

        elif "," in port:
            pl = port.split(",")
            int_map = map(int, pl)
            dst_port = list(int_map)
            dst_port.sort()
            return dst_port

        elif port.isdigit():
            dst_port += [int(port)]
            return dst_port
    else:
        print(f"{c.C.RED}[✖]{c.C.END} Please enter a valid port number. '-p {port}' is not valid.\n"
              f'Examples:\n'
              f"'-p 80' scan port 80.\n"
              f"'-p 22-30' scan port range 22 to 30\n"
              f"'-p 80,443' scan port 80 and 443\n")
        exit()
