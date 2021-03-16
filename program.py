import argparse
import ipaddress
from coolstuf import banner
from coolstuf import tcp_connect


parser = argparse.ArgumentParser(
    description=banner.banner()
)

# Get arguments for the program
parser.add_argument('-i', '--ip', metavar='ip', required=True, help='The IP address to scan')
parser.add_argument('-t', '--type', metavar='type', required=True,
                    choices={'tcp-connect', 'tcp-syn', 'udp', 'xmas'}, help='What kind of scan?')
parser.add_argument('-l', '--log', metavar='log', required=False,
                    choices={'json', 'xml', 'none'}, default='none', help='Do you want to log? Default none.')
parser.add_argument('-p', '--port', metavar='port', required=True, help='What port number to scan?')
parser.add_argument('-to', '--timeout', metavar='timeout', required=False,
                    default=6, help='Specify a timeout, default 6.')
parser.add_argument('-v', '--verbose', metavar='verbose', required=False,
                    default=0, choices={0, 1, 2, 3}, help='Level of verbosity, from 0 (almost mute) to 3 (verbose)')

args = parser.parse_args()

# Check for valid IPv4 Address
try:
    ipaddress.ip_address(args.ip)
except ValueError:
    print("Please enter a valid IPv4 address")

dst_port = int(args.port)

print(f'[+] Target: {args.ip}')
print(f'[+] Scan started')

if args.type == 'tcp-connect':
    tcp_connect.tcp_connect_scan(args.ip, args.log, dst_port, args.timeout, args.verbose)
