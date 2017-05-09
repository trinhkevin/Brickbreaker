#!/usr/bin/env python2.7

'''
    Player
    PyGame + Twisted
    Brian Byrne & Kevin Trinh
    05/10/2017
'''

from __future__ import print_function

import sys, os
import getopt
import json

from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from brickbreaker import BrickBreaker

from twisted.python import log
log.startLogging(sys.stdout)

# Connect --------------------------------------

class Connect(Protocol):
    def __init__(self):
        self.brickBreaker = BrickBreaker(self, 2)

    def connectionMade(self):
        print("Game connection established")
        self.brickBreaker.initialize()
        self.brickBreaker.initializeBricks()
        LoopingCall(self.brickBreaker.play).start(0.015)

    def dataReceived(self, data):
        self.brickBreaker.dataReceived(data)

    def connectionLost(self, reason):
        Factory.clients.remove(self)

    def write(self, data):
        self.transport.write(data)

class ConnectFactory(ClientFactory):
    def __init__(self):
        self.connect = Connect()

    def buildProtocol(self, address):
        return self.connect

# Listen ---------------------------------------

class Listen(Protocol):
    def __init__(self):
        self.brickBreaker = BrickBreaker(self, 1)

    def connectionMade(self):
        print("Game connection established")
        self.brickBreaker.initialize()
        self.brickBreaker.initializeBricks()
        LoopingCall(self.brickBreaker.dumpData).start(0.015)
        LoopingCall(self.brickBreaker.play).start(0.015)

    def dataReceived(self, data):
        self.brickBreaker.dataReceived(data)

    def connectionLost(self, reason):
        Factory.clients.remove(self)

    def write(self, data):
        self.transport.write(data)

class ListenFactory(Factory):
    def __init__(self):
        self.listen = Listen()

    def buildProtocol(self, address):
        return self.listen

def usage(exit_code=0):
    print('''Usage: {program} [-u USER -p PORT]

Options:

    -h          Show this help message
    -u          Set player: 1 for Listener, 2 for Connecter - Default = 1
    -p          TCP Port to use - Default = 40110

*Player 1 must be run first*'''.format(program=os.path.basename(sys.argv[0])))
    sys.exit(exit_code)

if __name__ == '__main__':

    # Default
    port    = 40110
    player  = 1
    server  = "ash.campus.nd.edu"

    # Parse Arguments
    try:
        options, arguments = getopt.getopt(sys.argv[1:], "u:p:hs:")
    except getopt.GetoptError as e:
        usage(1)

    for option, value in options:
        if option == '-u':
            player = int(value)
        elif option == '-s':
            server = value
        elif option == '-p':
            port = int(value)
        elif option == '-h':
            usage(0)
        else:
            usage(1)

    # Run
    if player == 1:
        reactor.listenTCP(port, ListenFactory())
    elif player == 2:
        reactor.connectTCP(server, port, ConnectFactory())

    reactor.run()
