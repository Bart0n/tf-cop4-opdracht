# TF-COP4.0 Port-Scan!

When used properly, TF-COP4.0 Port-Scan helps protect your network from invaders. But when used improperly, 
TF-COP4.0 Port-Scan can (in rare cases) get you sued, fired, expelled, jailed, or banned by your ISP!

## Usage:
To run the program, simple use:`program.py -h`for help output.

This program has the following statements:

####Required:

`-i`: IP address to scan

`-t`: Type of scan (tcp-connect, tcp-syn, udp, xmas)

`-p`: Port to scan

####Mandatory
`-to`: Timeout in seconds

`-sc`: Show closed ports

`-v`: Level of verbose 

`-l`: Log type and location

`-rd`: Remove database

####Examples
Scan port 1 through 100, timeout of 1 second, showing closed ports and log to target.json:

`program.py -i 192.168.1.1 -t tcp-connect -p 1-100 -to 1 -sc -l json target.json`
