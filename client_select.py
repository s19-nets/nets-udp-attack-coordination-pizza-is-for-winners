from socket import *
from select import select
import time


address = ('localhost', 50001)


def run():
    host = ''
    port = 8888
    size = 8000
    backlog = 5

    # create udp socket
    # udp = socket(AF_INET, SOCK_DGRAM)
    # udp.bind(('localhost', port))  # Client connects automatically?
    udp = socket(AF_INET, SOCK_DGRAM)
    udp.bind(address)

    input = [udp]
    output = [socket(AF_INET, SOCK_DGRAM)]

    while True:
        time.sleep(1)
        inputready, outputready, exceptready = select(input, output, [], 5)

        if inputready:
            data, addr = udp.recvfrom(1024)
            if data:
                print(data)
            print("No data :(")

        if outputready:
            send_udp()


def send_udp():
    s = socket(AF_INET, SOCK_DGRAM)
    data = "UDP "*4
    print("sending")
    s.sendto(data.encode(), ('localhost', 50002))
    s.close()


def read_udp(s):
    data, addr = s.recvfrom(8000)
    print("Recv UDP:'%s'" % data)



# UDP SEND
run()
