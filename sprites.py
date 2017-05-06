'''
    Objects
    Pygame + Twisted
    Brian Byrne & Kevin Trinh
    05/10/2017
'''

import os, sys
import math
import pygame
from pygame.locals import *
import constants
from random import randint

class Background(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image  = pygame.image.load(image)
        self.rect   = self.image.get_rect()
        self.rect.left, self.rect.top = 0,0

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self, playerNumber, x, player):
        pygame.sprite.Sprite.__init__(self)
        pygame.font.init()
        self.playerNumber   = playerNumber
        self.player         = player
        self.font           = pygame.font.SysFont("monospace", constants.fontSize)
        self.image = self.font.render(self.getLives() + "PLAYER " + str(self.playerNumber) + " SCORE: " + str(self.player.score) + "    x" + self.getMultiplier(), True, constants.white)
        self.rect           = self.image.get_rect()
        self.rect.centerx   = x
        self.rect.y         = 0

    def update(self):
        self.image = self.font.render(self.getLives() + "PLAYER " + str(self.playerNumber) + " SCORE: " + str(self.player.score) + " x" + self.getMultiplier(), True, constants.white)

    def getLives(self):
        if self.player.lives == 3:
            return "♥♥♥"
        elif self.player.lives == 2:
            return " ♥♥"
        elif self.player.lives == 1:
            return "   ♥"
        else:
            return "   "

    def getMultiplier(self):
        return str(self.player.multiplier)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.width  = constants.platformWidth
        self.height = constants.platformHeight
        self.image  = pygame.Surface([self.width, self.height])
        self.image.fill(constants.white)
        self.rect   = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.rect.x -= constants.platformSpeed
                if self.rect.x < 0:
                    self.rect.x = 0
            if event.key == pygame.K_RIGHT:
                self.rect.x += constants.platformSpeed
                if self.rect.x > constants.width - constants.platformWidth:
                    self.rect.x = constants.width - constants.platformWidth

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, gray):
        pygame.sprite.Sprite.__init__(self)
        self.width  = constants.brickWidth - constants.brickBorder
        self.height = constants.brickHeight - constants.brickBorder
        self.image = pygame.Surface([self.width, self.height])
        color = randint(0, 99)
        # Set Random Block
        self.rainbow = False
        self.current = 0
        self.life    = 1
        self.color = constants.yellow
        if gray is False:
            if color > 92:
                self.color = constants.red
            elif color > 82:
                self.color = constants.green
            elif color > 72:
                self.color = constants.blue
            elif color > 32:
                self.color = constants.yellow
            elif color > 12:
                self.color = constants.purple
                self.life  = 2
            elif color > 2:
                self.color = constants.orange
                self.life  = 3
            else:
                self.color = constants.colors[self.current]
                self.rainbow = True
                self.life  = 3
        # If Wall is to be Gray
        else:
            self.color = constants.gray
            self.life  = -1
            self.rainbow = False
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # If it's the Rainbow Block, Cycle
        # Through Colors
        if self.life <= 0 and self.color != constants.gray:
            self.kill()
        if self.rainbow:
            self.current += 1
            if self.current > constants.ncolors - 1:
                self.current = self.current % (constants.ncolors - 1)
            self.color = constants.colors[self.current]
            self.image.fill(self.color)

class Ball(pygame.sprite.Sprite):
    def __init__(self, platform):
        pygame.sprite.Sprite.__init__(self)
        self.platform       = platform
        self.radius         = constants.ballRadius
        self.color          = constants.white
        self.isOnPlatform   = True
        self.other          = None
        self.image          = pygame.Surface([constants.ballRadius, constants.ballRadius])
        self.rect           = self.image.get_rect()
        self.rect.centerx   = self.platform.rect.centerx
        self.instatimer     = 0
        self.blacktimer     = 0
        self.speed          = 1
        self.speedChanged   = False
        if self.platform.player.number == 1:
            self.rect.centery     = self.platform.rect.centery + constants.ballRadius + constants.platformHeight / 2
        elif self.platform.player.number == 2:
            self.rect.centery     = self.platform.rect.centery - constants.ballRadius - constants.platformHeight / 2
        self.angle = randint(60,120) * (math.pi/180)
        self.xVel  = constants.ballVelocity
        self.yVel  = constants.ballVelocity

    def update(self, event=None):
        # Black Timer
        if self.blacktimer > 0:
            self.blacktimer -= 1
            if self.blacktimer <= 0:
                self.color = constants.white

        # Instakill Timer
        if self.instatimer > 0:
            self.instatimer -= 1
            if self.instatimer <= 0:
                self.color = constants.white

        # Ball Starts Out On Platform
        if self.isOnPlatform:
            self.platform.player.timer      = 0
            self.platform.player.multiplier = 1
            if event:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isOnPlatform = False
                    if event.key == pygame.K_LEFT or event.key== pygame.K_RIGHT:
                        self.rect.centerx = self.platform.rect.centerx
                        if self.platform.player.number == 1:
                            self.rect.centery = self.platform.rect.centery + constants.ballRadius + constants.platformHeight / 2
                        elif self.platform.player.number == 2:
                            self.rect.centery = self.platform.rect.centery - constants.ballRadius - constants.platformHeight / 2
        # Normal Movement
        else:
            # Increment Timer Not Dead
            # and Set Multiplier
            self.platform.player.timer += 1
            if (self.platform.player.timer / 60) >= 25:
                self.platform.player.multiplier = 32
            elif (self.platform.player.timer / 60) >= 20:
                self.platform.player.multiplier = 16
            elif (self.platform.player.timer / 60) >= 15:
                self.platform.player.multiplier = 8
            elif (self.platform.player.timer / 60) >= 10:
                self.platform.player.multiplier = 4
            elif (self.platform.player.timer / 60) >= 5:
                self.platform.player.multiplier = 2
            else:
                self.platform.player.multiplier = 1

            # Move Ball
            if self.platform.player.number == 1:
                self.rect.centerx += self.speed * self.xVel * math.cos(self.angle)
                self.rect.centery += self.speed * self.yVel * math.sin(self.angle)
            elif self.platform.player.number == 2:
                self.rect.centerx -= self.speed * self.xVel * math.cos(self.angle)
                self.rect.centery -= self.speed * self.yVel * math.sin(self.angle)

            # Vertical Wall Collisions
            if self.rect.centerx + constants.ballRadius > constants.width:
                self.xVel *= -1
                self.rect.centerx = constants.width - constants.ballRadius
            elif self.rect.centerx - constants.ballRadius < 0:
                self.xVel *= -1
                self.rect.centerx = constants.ballRadius

            # Horizontal Wall Collision - aka Dead
            elif self.rect.centery + constants.ballRadius > constants.height or self.rect.centery - constants.ballRadius < 0:
                self.platform.player.lives      -= 1
                self.isOnPlatform               = True
                self.speed                      = 1

    def collided(self, collide, ctype):
        if ctype == "platform":
            # Change Speed Back, if Changed
            if self.speedChanged:
                self.speed = 1
                if self.color != constants.black or self.color != constants.red:
                    self.color = constants.white
        elif ctype == "brick":
            # Damage
            if self.instatimer and collide.color != constants.gray:
                collide.life -= 100
            elif collide.color != constants.gray:
                collide.life -= 1

            # Brick Break
            if collide.life <= 0:
                if collide.rainbow:
                    self.platform.player.score += self.platform.player.multiplier * 100
                    self.other.turnBlack()
                if collide.color == constants.red:
                    self.platform.player.score += self.platform.player.multiplier * 50
                    self.fastBall()
                elif collide.color == constants.green:
                    self.platform.player.score += self.platform.player.multiplier * 30
                    self.platform.player.addLife()
                elif collide.color == constants.blue:
                    self.platform.player.score += self.platform.player.multiplier * 50
                    self.setInstakill()
                elif collide.color == constants.yellow:
                    self.platform.player.score += self.platform.player.multiplier * 10
                elif collide.color == constants.purple:
                    self.platform.player.score += self.platform.player.multiplier * 20
                elif collide.color == constants.orange:
                    self.platform.player.score += self.platform.player.multiplier * 50
                    self.setInstakill()

        # Collision Side
        # From: https://gamedev.stackexchange.com/questions/22609/breakout-collision-detecting-the-side-of-collision
        if self.rect.centery <= collide.rect.centery - (collide.height/2) or self.rect.centery > collide.rect.centery + (collide.height/2):
            self.yVel *= -1
        elif self.rect.centerx < collide.rect.centerx or self.rect.centerx > collide.rect.centerx:
            self.xVel *= -1

    def turnBlack(self):
        self.blacktimer = 3 * 60
        self.color      = constants.black

    def setInstakill(self):
        self.instatimer = 3 * 60
        self.color      = constants.red

    def fastBall(self):
        self.speed          = constants.fastSpeed
        self.color          = constants.yellow
        self.speedChanged   = True

    def slowBall(self):
        self.speed          = constants.slowSpeed
        self.color          = constants.blue
        self.speedChanged   = True

class Player():
    def __init__(self, number):
        self.number     = number
        self.score      = 0
        self.lives      = 3
        self.multiplier = 1
        self.timer      = 0

    def addLife(self):
        self.lives += 1
        if self.lives > 3:
            self.lives = 3
