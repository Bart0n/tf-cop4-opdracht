import argparse
import datetime
import concurrent.futures
import time
from coolstuf import checkvalidip
from coolstuf import banner
from coolstuf import tcp_connect
from coolstuf import tcp_syn
from coolstuf import udp
from coolstuf import tcp_xmas
from coolstuf import ports
from coolstuf import database
from coolstuf import log_handler
from coolstuf import color as c


# Set date
date = datetime.datetime.now()
date = date.strftime("%Y-%m-%d %H:%M:%S")

# Set start time, so we can show off with our ultra fast scanner
start_time = time.time()

# A good program, needs a good banner
parser = argparse.ArgumentParser(description=print(banner.banner()))
# Get arguments for the program, also do input sanitization for some fields (choices)
parser.add_argument('-i', metavar='ip', required=True,
                    help='The IP address to scan')
parser.add_argument('-t', metavar='type', required=True, choices={'tcp-connect', 'tcp-syn', 'udp', 'xmas'},
                    help="What kind of scan? Ex: '-t tcp-connect', '-t tcp-syn', '-t udp' or '-t xmas'")
parser.add_argument('-p', metavar='port', required=True,
                    help="What port number to scan? Ex: '-p 80,443' or '-p 120-130'")
parser.add_argument('-to', metavar='timeout', required=False, default=6, type=int, choices=range(1, 10),
                    help='Specify a timeout (1-9), default 6.')
parser.add_argument('-sc', action='store_true',
                    help='Show closed ports')
parser.add_argument('-v', metavar='verbose', required=False, default=0, type=int, choices=range(0, 4),
                    help='Level of verbosity, from 0 (almost mute) to 3 (verbose)')
parser.add_argument('-l', metavar=('log', 'location'), required=False, nargs=2, default='none',
                    help="Do you want to log? Ex: '-l xml cop4.xml' or '-l json cop4.json'")
parser.add_argument('-rd', action='store_true',
                    help='Remove database')
cli_input = parser.parse_args()

# Check for valid IPv4 Address
if not checkvalidip.check_ip(cli_input.i)[0]:
    print(checkvalidip.check_ip(cli_input.i)[1])
    exit()

# Format the ports
dst_ports = ports.port_format(cli_input.p)
if not dst_ports[0]:  # If the dst_port[0] is set to False, print the error.
    print(dst_ports[1])
    exit()

# Database init
database_file = "database.sqlite3"
if cli_input.rd:  # If the database remove flag has been set, delete the database
    remove_database = database.delete_db(database_file)
    print(remove_database[1])
    # If the database cannot be removed (so remove_database[0] is set to False), exit the program.
    if not remove_database[0]:
        exit()
db = database.create_connection(database_file)
database.create_table(db)

print(f'[i] Target: {c.C.ITALIC}{cli_input.i}{c.C.END}')
print(f'[i] Scan started type: {c.C.ITALIC}{cli_input.t.upper()}{c.C.END} \n')

all_result = []  # Placeholder where all the results from the scans are stored
open_ports = []  # Placeholder where all the open ports are stored
closed_ports = []  # Placeholder where all the closed ports are stored
if cli_input.t == 'tcp-connect':
    # tcp_connect.tcp_connect_scan returns 3 values
    # Lets do some threading :)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = [executor.submit(tcp_connect.tcp_connect_scan, cli_input.i, dst_port, cli_input.to, cli_input.v) for
                  dst_port in dst_ports]
        # Don't use 'concurrent.futures.wait(future)', otherwise you don't see scan output on the fly.
        for results in future:
            tcp_con_single_port = results.result()
            # If port is closed (state 0) and -sc is been given, print it.
            if tcp_con_single_port[1] == 0 and cli_input.sc:
                print(c.C.RED, tcp_con_single_port[0])
            # If port is open (state 1), print it (always):
            elif tcp_con_single_port[1] == 1:
                print(c.C.YELLOW, tcp_con_single_port[0])
            # Grab all the results, and put it in.... all_result
            all_result += [tcp_con_single_port]

elif cli_input.t == 'tcp-syn':
    # tcp_syn.tcp_syn_scan returns 3 values
    # Lets do some threading :)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = [executor.submit(tcp_syn.tcp_syn_scan, cli_input.i, dst_port, cli_input.to, cli_input.v) for
                  dst_port in dst_ports]
        # Don't use 'concurrent.futures.wait(future)', otherwise you don't see scan output on the fly.
        for results in future:
            tcp_syn_single_port = results.result()
            # If port is closed (state 0) and -sc is been given, print it.
            if tcp_syn_single_port[1] == 0 and cli_input.sc:
                print(c.C.RED, tcp_syn_single_port[0])
            # If port is open (state 1), print it (always):
            elif tcp_syn_single_port[1] == 1:
                print(c.C.YELLOW, tcp_syn_single_port[0])
            # Grab all the results, and put it in.... all_result
            all_result += [tcp_syn_single_port]

elif cli_input.t == 'udp':
    # udp.udp_scan returns 3 values
    # Lets do some threading :)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = [executor.submit(udp.udp_scan, cli_input.i, dst_port, cli_input.to, cli_input.v) for
                  dst_port in dst_ports]
        # Don't use 'concurrent.futures.wait(future)', otherwise you don't see scan output on the fly.
        for results in future:
            udp_single_port = results.result()
            # If port is closed (state 0) and -sc is been given, print it.
            if udp_single_port[1] == 0 and cli_input.sc:
                print(c.C.RED, udp_single_port[0])
            # If port is open (state 1), print it (always):
            elif udp_single_port[1] == 1:
                print(c.C.YELLOW, udp_single_port[0])
            # Grab all the results, and put it in.... all_result
            all_result += [udp_single_port]

elif cli_input.t == 'xmas':
    # tcp_xmas.tcp_xmas_scan returns 3 values
    # Lets do some threading :)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = [executor.submit(tcp_xmas.tcp_xmas_scan, cli_input.i, dst_port, cli_input.to, cli_input.v) for
                  dst_port in dst_ports]
        # Don't use 'concurrent.futures.wait(future)', otherwise you don't see scan output on the fly.
        for results in future:
            tcp_xmas_single_port = results.result()
            # If port is closed (state 0) and -sc is been given, print it.
            if tcp_xmas_single_port[1] == 0 and cli_input.sc:
                print(c.C.RED, tcp_xmas_single_port[0])
            # If port is open (state 1), print it (always):
            elif tcp_xmas_single_port[1] == 1:
                print(c.C.YELLOW, tcp_xmas_single_port[0])
            # Grab all the results, and put it in.... all_result
            all_result += [tcp_xmas_single_port]

# Quick for loop to divide the open and closed port for logging
for x in all_result:
    # Port Open
    if x[1] == 1:  # Item [1] contains a 1 if the port is open
        open_ports += [x[2]]  # Item [2] contains the port that is been scanned
    # Port Closed
    if x[1] == 0:  # Item [1] contains a 0 if the port is open
        closed_ports += [x[2]]  # Item [2] contains the port that is been scanned

# A nice sum at the end of the scan
print(f"\n{c.C.YELLOW}[✓]{c.C.END} {c.C.BOLD}COP-Scan{c.C.END} finished in {round(time.time() - start_time,2)} seconds."
      f"\n{c.C.YELLOW}[✓]{c.C.END} Scanned {c.C.UNDERLINE}{c.C.GREEN}{len(dst_ports)}{c.C.END} port(s). "
      f"{c.C.YELLOW}{len(open_ports)} ports open, {c.C.RED}{len(closed_ports)} closed.{c.C.END}")

# Put data is database, return value is the database row.
database_row = database.insert_data(db, date, str(cli_input.i), str(cli_input.t), str(cli_input.p),
                                    str(open_ports), str(closed_ports))
print(f"{c.C.YELLOW}[✓]{c.C.END} Saved to database row: {database_row}")

# Parse it to the log handler & print out the logging result (value [0] stores a True/False if logging is done)
logging_result = log_handler.write_output(date, cli_input.i, cli_input.t, cli_input.p, cli_input.to, open_ports,
                                          closed_ports, cli_input.l[1], cli_input.l[0])
print(logging_result[1])
