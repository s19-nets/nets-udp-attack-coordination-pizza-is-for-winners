#! /usr/bin/env python3
from socket import *

# default params
serverAddr = ('localhost', 50000)       

import sys, re                          

def usage():
    print(("usage: %s [--serverAddr host:port]"  % sys.argv[0]))
    sys.exit(1)

try:
    args = sys.argv[1:]
    while args:
        sw = args[0]; del args[0]
        if sw == "--serverAddr":
            addr, port = re.split(":", args[0]); del args[0]
            serverAddr = (addr, int(port))
        else:
            print(("unexpected parameter %s" % args[0]))
            usage();
except:
    usage()



clientSocket = socket(AF_INET, SOCK_DGRAM)
message = eval(input("Input lowercase msg:"))
clientSocket.sendto(message.encode(), serverAddr)
modifiedMessage, serverAddrPort = clientSocket.recvfrom(2048)
print(("Modified message from %s is <%s>" % (repr(serverAddrPort), modifiedMessage)))
