#!/usr/bin/env python3

'''
    BrickBreaker class
    Pygame + Twisted
    Brian Byrne & Kevin Trinh
    05/10/2017
'''

from __future__ import print_function
import sys, os
import json
import pygame
from pygame.locals import *
import sprites
import constants

class BrickBreaker:

    def __init__(self, connection, playerNumber):
        # Initialize Window
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Brickbreaker')
        self.connection     = connection
        self.playerNumber   = playerNumber

    def initialize(self):
        self.size   = self.width, self.height = constants.width, constants.height
        self.screen = pygame.display.set_mode(self.size)
        self.clock  = pygame.time.Clock()

        # Initialize Background
        self.background = sprites.Background('stars.png')

        # Initialize Players
        self.player1 = sprites.Player(1)
        self.player2 = sprites.Player(2)

        # Initialize Scoreboard
        self.scoreboard1 = sprites.Scoreboard(1, constants.width/4, self.player1)
        self.scoreboard2 = sprites.Scoreboard(2, 3*constants.width/4, self.player2)

        # Initialize Platforms
        self.platforms = pygame.sprite.Group()
        self.platform1 = sprites.Platform(constants.width/2, 50, self.player1)
        self.platform2 = sprites.Platform(constants.width/2, constants.height - 50, self.player2)
        self.platforms.add(self.platform1)
        self.platforms.add(self.platform2)

        # Initialize Balls
        self.balls = pygame.sprite.Group()
        self.ball1 = sprites.Ball(self.platform1)
        self.ball2 = sprites.Ball(self.platform2)
        self.ball1.other = self.ball2
        self.ball2.other = self.ball1
        self.balls.add(self.ball1)
        self.balls.add(self.ball2)

    # Initialize Bricks
    def initializeBricks(self):
        self.bricks = pygame.sprite.Group()
        for x in range(0,16):
            for y in range(0,15):
                if y == 7:
                    brick = sprites.Brick(x * constants.brickWidth, 200 + y * constants.brickHeight, True)
                else:
                    brick = sprites.Brick(x * constants.brickWidth, 200 + y * constants.brickHeight, False)
                self.bricks.add(brick)

    def main(self):
        # Check for Win (technically checking for a loss)
        if self.player1.lives <= 0:
            print("Player 2 Wins!")
            self.connection.write("Player 2 Wins!")
            pygame.quit()
        elif self.player2.lives <= 0:
            print("Player 1 Wins!")
            self.connection.write("Player 1 Wins!")
            pygame.quit()

        # User Input Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.playerNumber == 1:
                        self.platform1.moveLeft()
                        self.connection.write("move left")
                    elif self.playerNumber == 2:
                        self.platform2.moveLeft()
                        self.connection.write("move left")
                if event.key == pygame.K_RIGHT:
                    if self.playerNumber == 1:
                        self.platform1.moveRight()
                        self.connection.write("move right")
                    elif self.playerNumber == 2:
                        self.platform2.moveRight()
                        self.connection.write("move right")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.playerNumber == 1:
                        self.ball1.releaseBall()
                        self.connection.write("release ball")
                    elif self.playerNumber == 2:
                        self.ball2.releaseBall()
                        self.connection.write("release ball")

        # Tick
        self.scoreboard1.update()
        self.scoreboard2.update()
        self.ball1.update()
        self.ball2.update()
        self.bricks.update()

        # Check for Collisions and Calculate Points
        for ball in self.balls:
            for brick in pygame.sprite.spritecollide(ball, self.bricks, False, self.intersects):
                ball.collided(brick, "brick")
            for platform in pygame.sprite.spritecollide(ball, self.platforms, False, self.intersects):
                ball.collided(platform, "platform")

    def draw(self):
        # Draw Sprites
        self.screen.fill(constants.black)
        self.screen.blit(self.background.image, self.background.rect)
        self.screen.blit(self.scoreboard1.image, self.scoreboard1.rect)
        self.screen.blit(self.scoreboard2.image, self.scoreboard2.rect)
        self.screen.blit(self.platform1.image, self.platform1.rect)
        self.screen.blit(self.platform2.image, self.platform2.rect)
        for brick in self.bricks:
            self.screen.blit(brick.image, brick.rect)
        pygame.draw.circle(self.screen, self.ball1.color, self.ball1.rect.center, self.ball1.radius)
        pygame.draw.circle(self.screen, self.ball2.color, self.ball2.rect.center, self.ball2.radius)
        pygame.display.flip()

    def dataReceived(self, data):
        if data == "move left":
            if self.playerNumber == 1:
                self.platform2.moveLeft()
            elif self.playerNumber == 2:
                self.platform1.moveLeft()
        elif data == "move right":
            if self.playerNumber == 1:
                self.platform2.moveRight()
            elif self.playerNumber == 2:
                self.platform1.moveRight()
        elif data == "release ball":
            if self.playerNumber == 1:
                self.ball2.releaseBall()
            elif self.playerNumber == 2:
                self.ball1.releaseBall()
        elif data == "Player 1 Wins!":
            print("Player 1 Wins!")
            sys.exit()
        elif data == "Player 2 Wins!":
            print("Player 2 Wins!")
            sys.exit()
        else:
            try:
                data = json.loads(data)
                self.bricks.empty()
                for b in data["bricks"]:
                    brick = sprites.Brick(b["rectX"] * constants.brickWidth, 200 + b["rectY"] * constants.brickHeight, True)
                    #brick.width = b["width"]
                    #brick.height = b["height"]
                    #brick.image = b["image"]
                    brick.rainbow = b["rainbow"]
                    brick.current = b["current"]
                    brick.life = b["life"]
                    brick.color = b["color"]
                    brick.image.fill(brick.color)
                    brick.rect.x = b["rectX"]
                    brick.rect.y = b["rectY"]
                    self.bricks.add(brick)
                    print("ADDED BRICK")

                #self.ball1.platform = data["ball1"]["platform"]
                self.ball1.radius = data["ball1"]["radius"]
                self.ball1.color = data["ball1"]["color"]
                self.ball1.isOnPlatform = data["ball1"]["isOnPlatform"]
                #self.ball1.other = data["ball1"]["other"]
                #self.ball1.image = data["ball1"]["image"]
                self.ball1.rect.x = data["ball1"]["rectX"]
                self.ball1.rect.y = data["ball1"]["rectY"]
                self.ball1.instatimer = data["ball1"]["instatimer"]
                self.ball1.blacktimer = data["ball1"]["blacktimer"]
                self.ball1.speed = data["ball1"]["speed"]
                self.ball1.speedChanged = data["ball1"]["speedChanged"]
                self.ball1.angle = data["ball1"]["angle"]
                self.ball1.xVel = data["ball1"]["xVel"]
                self.ball1.yVel = data["ball1"]["yVel"]
                pygame.draw.circle(self.screen, self.ball1.color, self.ball1.rect.center, self.ball1.radius)

                #self.ball2.platform = data["ball2"]["platform"]
                self.ball2.radius = data["ball2"]["radius"]
                self.ball2.color = data["ball2"]["color"]
                self.ball2.isOnPlatform = data["ball2"]["isOnPlatform"]
                #self.ball2.other = data["ball2"]["other"]
                #self.ball2.image = data["ball2"]["image"]
                self.ball2.rect.x = data["ball2"]["rectX"]
                self.ball2.rect.y = data["ball2"]["rectY"]
                self.ball2.instatimer = data["ball2"]["instatimer"]
                self.ball2.blacktimer = data["ball2"]["blacktimer"]
                self.ball2.speed = data["ball2"]["speed"]
                self.ball2.speedChanged = data["ball2"]["speedChanged"]
                self.ball2.angle = data["ball2"]["angle"]
                self.ball2.xVel = data["ball2"]["xVel"]
                self.ball2.yVel = data["ball2"]["yVel"]
                pygame.draw.circle(self.screen, self.ball2.color, self.ball2.rect.center, self.ball2.radius)

                self.player1.number = data["player1"]["number"]
                self.player1.score = data["player1"]["score"]
                self.player1.lives = data["player1"]["lives"]
                self.player1.multiplier = data["player1"]["multiplier"]
                self.player1.timer = data["player1"]["timer"]

                self.player2.number = data["player2"]["number"]
                self.player2.score = data["player2"]["score"]
                self.player2.lives = data["player2"]["lives"]
                self.player2.multiplier = data["player2"]["multiplier"]
                self.player2.timer = data["player2"]["timer"]

                #self.platform1.player = data["platform1"]["player"]
                #self.platform1.width = data["platform1"]["width"]
                #self.platform1.height = data["platform1"]["height"]
                #self.platform1.image = data["platform1"]["image"]
                self.platform1.rect.x = data["platform1"]["rectX"]
                self.platform1.rect.y = data["platform1"]["rectY"]

                #self.platform2.player = data["platform2"]["player"]
                #self.platform2.width = data["platform2"]["width"]
                #self.platform2.height = data["platform2"]["height"]
                #self.platform2.image = data["platform2"]["image"]
                self.platform2.rect.x = data["platform2"]["rectX"]
                self.platform2.rect.y = data["platform2"]["rectY"]
            except:
                pass

    def play(self):
        self.main()
        self.draw()

    def dumpData(self):

        data = {}
        data["bricks"] = []
        for brick in self.bricks:
            b = {}
            #b["width"] = brick.width
            #b["height"] = brick.height
            #b["image"] = brick.image
            b["rainbow"] = brick.rainbow
            b["current"] = brick.current
            b["life"] = brick.life
            b["color"] = brick.color
            b["rectX"] = brick.rect.x
            b["rectY"] = brick.rect.y
            data["bricks"].append(b)

        data["ball1"] = {}
        #data["ball1"]["platform"] = self.ball1.platform
        data["ball1"]["radius"] = self.ball1.radius
        data["ball1"]["color"] = self.ball1.color
        data["ball1"]["isOnPlatform"] = self.ball1.isOnPlatform
        #data["ball1"]["other"] = self.ball1.other
        #data["ball1"]["image"] = self.ball1.image
        data["ball1"]["rectX"] = self.ball1.rect.x
        data["ball1"]["rectY"] = self.ball1.rect.y
        data["ball1"]["instatimer"] = self.ball1.instatimer
        data["ball1"]["blacktimer"] = self.ball1.blacktimer
        data["ball1"]["speed"] = self.ball1.speed
        data["ball1"]["speedChanged"] = self.ball1.speedChanged
        data["ball1"]["angle"] = self.ball1.angle
        data["ball1"]["xVel"] = self.ball1.xVel
        data["ball1"]["yVel"] = self.ball1.yVel

        data["ball2"] = {}
        #data["ball2"]["platform"] = self.ball2.platform
        data["ball2"]["radius"] = self.ball2.radius
        data["ball2"]["color"] = self.ball2.color
        data["ball2"]["isOnPlatform"] = self.ball2.isOnPlatform
        #data["ball2"]["other"] = self.ball2.other
        #data["ball2"]["image"] = self.ball2.image
        data["ball2"]["rectX"] = self.ball2.rect.x
        data["ball2"]["rectY"] = self.ball2.rect.y
        data["ball2"]["instatimer"] = self.ball2.instatimer
        data["ball2"]["blacktimer"] = self.ball2.blacktimer
        data["ball2"]["speed"] = self.ball2.speed
        data["ball2"]["speedChanged"] = self.ball2.speedChanged
        data["ball2"]["angle"] = self.ball2.angle
        data["ball2"]["xVel"] = self.ball2.xVel
        data["ball2"]["yVel"] = self.ball2.yVel

        data["player1"] = {}
        data["player1"]["number"] = self.player1.number
        data["player1"]["score"] = self.player1.score
        data["player1"]["lives"] = self.player1.lives
        data["player1"]["multiplier"] = self.player1.multiplier
        data["player1"]["timer"] = self.player1.timer

        data["player2"] = {}
        data["player2"]["number"] = self.player2.number
        data["player2"]["score"] = self.player2.score
        data["player2"]["lives"] = self.player2.lives
        data["player2"]["multiplier"] = self.player2.multiplier
        data["player2"]["timer"] = self.player2.timer

        data["platform1"] = {}
        #data["platform1"]["player"] = self.platform1.player
        #data["platform1"]["width"] = self.platform1.width
        #data["platform1"]["height"] = self.platform1.height
        #data["platform1"]["image"] = self.platform1.image
        data["platform1"]["rectX"] = self.platform1.rect.x
        data["platform1"]["rectY"] = self.platform1.rect.y

        data["platform2"] = {}
        #data["platform2"]["player"] = self.platform2.player
        #data["platform2"]["width"] = self.platform2.width
        #data["platform2"]["height"] = self.platform2.height
        #data["platform2"]["image"] = self.platform2.image
        data["platform2"]["rectX"] = self.platform2.rect.x
        data["platform2"]["rectY"] = self.platform2.rect.y

        self.connection.write(json.dumps(data))

    # Intersection Between Circle and Rectangle
    # From: https://www.reddit.com/r/pygame/comments/2pxiha/rectanglar_circle_hit_detection/
    def intersects(self, circle, rect):
        circle_distance_x = abs(circle.rect.centerx-rect.rect.centerx)
        circle_distance_y = abs(circle.rect.centery-rect.rect.centery)
        if circle_distance_x > rect.width/2.0+constants.ballRadius or circle_distance_y > rect.height/2.0+constants.ballRadius:
            return False
        if circle_distance_x <= rect.width/2.0 or circle_distance_y <= rect.height/2.0:
            return True
        corner_x = circle_distance_x-rect.width/2.0
        corner_y = circle_distance_y-rect.height/2.0
        corner_distance_sq = corner_x**2.0 +corner_y**2.0
        return corner_distance_sq <= constants.ballRadius**2.0

if __name__ == '__main__':
    gs = BrickBreaker(1)
    gs.init_bricks()
    gs.main()
