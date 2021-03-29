import argparse
from coolstuf import checkvalidip
from coolstuf import banner
from coolstuf import tcp_connect
from coolstuf import ports
from coolstuf import database

parser = argparse.ArgumentParser(description=banner.banner())
# Get arguments for the program
parser.add_argument('-i', metavar='ip', required=True, help='The IP address to scan')
parser.add_argument('-t', metavar='type', required=True, choices={'tcp-connect', 'tcp-syn', 'udp', 'xmas'},
                    help="What kind of scan? Ex: '-t tcp-connect', '-t tcp-syn', '-t udp' or '-t xmas'")
parser.add_argument('-p', metavar='port', required=True,
                    help="What port number to scan? Ex: '-p 80,443' or '-p 120-130'")
parser.add_argument('-to', metavar='timeout', required=False,
                    default=6, type=int, choices=range(1, 10), help='Specify a timeout (1-9), default 6.')
parser.add_argument('-sc', action='store_true', help='Show closed ports')
parser.add_argument('-v', metavar='verbose', required=False, default=0, type=int, choices=range(0, 4),
                    help='Level of verbosity, from 0 (almost mute) to 3 (verbose)')
parser.add_argument('-l', metavar=('log', 'location'), required=False,
                    nargs=2, default='none none', help="Do you want to log? Ex: '-l xml cop4.xml' or '-l json cop4.json'")
parser.add_argument('-rd', action='store_true', help='Remove database')
args = parser.parse_args()

# Check for valid IPv4 Address
if not checkvalidip.check_ip(args.i):
    exit()

# Format the ports
dst_port = ports.port_format(args.p)

# Remove database if requested
database_file = "database.sqlite3"
if args.rd:
    database.delete_db(database_file)

# Create database connection
db = database.create_connection(database_file)

# Create tables in database, if not exist
database.create_table(db)

print(f'[+] Target: {args.i}')
print(f'[+] Scan started \n')

if args.t == 'tcp-connect':
    tcp_connect.tcp_connect_scan(args.i, args.l, dst_port, args.to, args.v, args.sc, db)
    schijft naar db
    schrijf naar xml
elif args.t == 'tcp-syn':
    print("TCP-Syn Scan")
elif args.t == 'udp':
    print("UDP Scan")
elif args.t == 'xmas':
    print("XMAS Scan")
