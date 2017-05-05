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

from brickbreaker import GameSpace

# Client ---------------------------------------

class Client(Protocol):
    def __init__(self):
    def connectionMade(self):
    def dataReceived(self, data):

def ClientFactory(Factory):
    def __init__(self):
        self.client = Client()

    def buildProtocol(self, address):
        return self.client

# reactor.listenTCP(40110, Client())
# reactor.run()
