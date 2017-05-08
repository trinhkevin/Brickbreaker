'''
    Player
    PyGame + Twisted
    Brian Byrne & Kevin Trinh
    05/10/2017
'''

from __future__ import print_function

from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

from brickbreaker import BrickBreaker

class Player():
    pass

class Command(Protocol):
    pass

class CommandFactory(ClientFactory):
    pass

class Data(Protocol):
    pass

class DataFactory(ClientFactory):
    pass
