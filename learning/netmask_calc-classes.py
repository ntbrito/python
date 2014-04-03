#!/usr/bin/python
 
import sys
import math
from socket import inet_aton
 
USAGE = 'usage: {0} netmask\n'.format(sys.argv[0])
 
# validate input
if len(sys.argv) != 2:
    sys.stderr.write(USAGE)
    sys.exit(1)
 
netmask = sys.argv[1]

## Validate netmask
class testMask(Exception):
    def __init__(self, netmask):
        self.netmask = netmask
        if (int(self.netmask) > 32):
            exit(1)

##
## Define functions

## dotted to CIDR notation
def get_net_size(netmask):
    # validate input
    try:
        inet_aton(sys.argv[1])
    except:
        sys.stderr.write('Invalid netmask. \n')
        sys.stderr.write(USAGE)
        sys.exit(2)

    binary_str = ''
    for octet in netmask:
        binary_str += bin(int(octet))[2:].zfill(8)
    return str(len(binary_str.rstrip('0')))

## convert CIDR notation to Dotted (255.255.255.0)
def cidrToDotted(netmask):
    binary_str = ''
    step = 8
    quotient = 0
    dec_octet = [0, 0, 0, 0]
    netmaskDotted = ''

    ## validate input
    try:
        testMask(netmask) 
    except:
        sys.stderr.write('Invalid netmask. \n')
        sys.stderr.write(USAGE)
        sys.exit(2)

    for i in range (1, int(netmask) + 1):
        binary_str += str(1)

    ## quotient - number of full 8 bit octets
    quotient = int(netmask) // 8

    ## modulos - remaining bits for the last octet
    m = int(netmask) % 8
    octet = [binary_str[i:i+step] for i in range(0, int(netmask), step)]

    ## full 8 bit octets (netmask 8, 16, 24 and 32)
    if ( m == 0 ):
        for j in range (0, quotient):
            dec_octet[j] = int(str(octet[j]),2)

        netmaskDotted = '.'.join(map(str, dec_octet))

        return netmaskDotted

    else:
        for j in range (0, quotient):
            dec_octet[j] = int(str(octet[j]),2)

        """ last octet = 256 - 2^X """
        last_oct = 256 - 2**(8 - m)
        dec_octet[quotient] = last_oct
        netmaskDotted = '.'.join(map(str, dec_octet))

        return netmaskDotted

 
## Main
if len(sys.argv[1]) > 2:
    ## netmask
    netmask = sys.argv[1].split('.')

    ## print CIDR notation
    print "The netmask in CIDR notation is: " + get_net_size(netmask)
else:
    ## netmask
    netmask = sys.argv[1] 

    ## print Dotted notation
    print "The netmask in dotted notation is: " + cidrToDotted(netmask)
