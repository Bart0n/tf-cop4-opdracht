import argparse
import datetime
from coolstuf import checkvalidip
from coolstuf import banner
from coolstuf import tcp_connect
from coolstuf import ports
from coolstuf import database
from coolstuf import log_handler

# Set date
date = datetime.datetime.now()
date = date.strftime("%Y-%m-%d %H:%M:%S")

parser = argparse.ArgumentParser(description=banner.banner())
# Get arguments for the program
parser.add_argument('-i', metavar='ip', required=True, help='The IP address to scan')
parser.add_argument('-t', metavar='type', required=True, choices={'tcp-connect', 'tcp-syn', 'udp', 'xmas'}, help="What kind of scan? Ex: '-t tcp-connect', '-t tcp-syn', '-t udp' or '-t xmas'")
parser.add_argument('-p', metavar='port', required=True, help="What port number to scan? Ex: '-p 80,443' or '-p 120-130'")
parser.add_argument('-to', metavar='timeout', required=False, default=6, type=int, choices=range(1, 10), help='Specify a timeout (1-9), default 6.')
parser.add_argument('-sc', action='store_true', help='Show closed ports')
parser.add_argument('-v', metavar='verbose', required=False, default=0, type=int, choices=range(0, 4), help='Level of verbosity, from 0 (almost mute) to 3 (verbose)')
parser.add_argument('-l', metavar=('log', 'location'), required=False, nargs=2, default='none', help="Do you want to log? Ex: '-l xml cop4.xml' or '-l json cop4.json'")
parser.add_argument('-rd', action='store_true', help='Remove database')
args = parser.parse_args()

# Check for valid IPv4 Address
if not checkvalidip.check_ip(args.i):
    exit()

# Format the ports
dst_port = ports.port_format(args.p)

# Database init
database_file = "database.sqlite3"
if args.rd:
    database.delete_db(database_file)
db = database.create_connection(database_file)
database.create_table(db)

print(f'[+] Target: {args.i}')
print(f'[+] Scan started \n')

if args.t == 'tcp-connect':
    all_result = []
    for i in dst_port:
        fun_tcp_con_single_port = tcp_connect.tcp_connect_scan(args.i, i, args.to, args.v, args.sc)
        all_result += [fun_tcp_con_single_port]
    database.insert_data(db, date, str(args.i), str(args.t), str(dst_port), str(all_result))
    log_handler.write_output(date, args.i, args.t, dst_port, args.to, all_result, args.l[1], args.l[0])

elif args.t == 'tcp-syn':
    print("TCP-Syn Scan")
elif args.t == 'udp':
    print("UDP Scan")
elif args.t == 'xmas':
    print("XMAS Scan")
