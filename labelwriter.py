#!/usr/bin/env python

import socket
import sys

class Labelwriter:
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self._socket = socket.socket()
        self._socket.connect((self._ip,int(self._port)))

def main():
    print("running labelwriter module standalone")
    mylabelwriter = Labelwriter('192.168.1.3','9001')

if __name__ == '__main__':
    main()