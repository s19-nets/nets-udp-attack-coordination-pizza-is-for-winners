from socket import *
from select import select
import time

address = ('localhost', 50002)


def send_udp(data):
    s = socket(AF_INET, SOCK_DGRAM)
    s.sendto(data.encode(), ('localhost', 50001))
    s.close()


def read_udp(s):
    data, addr = s.recvfrom(8000)
    print("Recv UDP:'%s'" % data)


def run():

    # create udp socket
    udp = socket(AF_INET, SOCK_DGRAM)
    udp.bind(address)

    input = [udp]
    output = [socket(AF_INET, SOCK_DGRAM)]

    while True:
        time.sleep(1)
        inputready, outputready, exceptready = select(input, output, [], 5)

        print(inputready)
        print(outputready)

        for s in inputready:
            read_udp(s)

        for s in outputready:
            send_udp("server sends")


run()
