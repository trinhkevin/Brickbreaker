'''
    Server
    PyGame + Twisted
    Brian Byrne & Kevin Trinh
    05/10/2017
'''

from __future__ import print_function
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

from brickbreaker import BrickBreaker

# Server ---------------------------------------

class Server(Protocol):
    def __init__(self):
        self.queue = DeferredQueue()
        

    def listen(self):
        reactor.listenTCP(40125, CommandFactory(self, 1))
        reactor.listenTCP(41125, CommandFactory(self, 2))
        reactor.run()

# Command --------------------------------------

class Command(Protocol):
    def __init__(self, server, player):
        self.server = server
        self.player = player

    def connectionMade(self):
        self.transport.write("Command made")
        if self.player == 1:
            reactor.listenTCP(40110, DataFactory(self, self.server, self.player))
        if self.player == 2:
            reactor.listenTCP(41110, DataFactory(self, self.server, self.player))

    def dataReceived(self, data):
        self.queu.put(data)

    def startForwarding(self):
        self.queu.get().addCallback(self.forwardData)

    def forwardData(self, data):
        self.data.listen.transport.write(data)
        self.queue.get().addCallback(self.forwardData)

class CommandFactory(Factory):
    def __init__(self, server, player):
        self.command = Command(server, player)
    
    def buildProtocol(self, address):
        return self.command

# Data -----------------------------------------

class Data(Protocol):
    def __init__(self, command, server, player):
        self.server = server
        self.command = command
        self.player = player

    def connectionMade(self):
        self.command.startForwarding()

    def dataReceived(self, data):
        self.server.queue.put(data)

class DataFactory(Factory):
    def __init__(self, command, server, player):
        self.data = Data(command, server, player)

    def buildProtocol(self):
        return self.data

if __name__ == '__main__':
    server = Server()
    server.listen()
