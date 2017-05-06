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

# Client ---------------------------------------

class Server(Protocol):
    def __init__(self):
        self.data_queue = DeferredQueue()
        self.players = 0

    def listen(self):
        reactor.listenTCP(40125, CommandFactory(self))
        reactor.listenTCP(41125, CommandFactory(self))
        reactor.run()

class Command(Protocol):
    def __init__(self, server):
        self.server = server

    def connectionMade(self):
        self.transport.write("Command made")
        self.server.players += 1
        if self.server.players == 2:
            self.transport.write("DATA")
            reactor.listenTCP(40110, DataFactory(self.server))
            reactor.listenTCP(41110, DataFactory(self.server))

class CommandFactory(Factory):
    def __init__(self, server):
        self.server = server

    def buildProtocol(self, address):
        return Command( self.server)

class Data(Protocol):
    def __init__(self, server):
        self.server = server

    def connectionMade(self):
        self.transport.write("Data made")

    def dataReceived(self):
       pass 

class DataFactory(Factory):
    def __init__(self, server):
        self.server = server

    def buildProtocol(self):
        return Data(self.server)

if __name__ == '__main__':
    server = Server()
    server.listen()

# reactor.listenTCP(40110, Client())
# reactor.run()
