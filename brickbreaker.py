#!/usr/bin/env python3

'''
    BrickBreaker class
    Pygame + Twisted
    Brian Byrne & Kevin Trinh
    05/10/2017
'''

import os, sys
import pygame
from pygame.locals import *
import sprites
import constants

# Intersection Between Circle and Rectangle
# From: https://www.reddit.com/r/pygame/comments/2pxiha/rectanglar_circle_hit_detection/
def intersects(circle, rect):
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

class BrickBreaker:
    def run(self):
        # Initialize Window
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Brickbreaker')
        self.size   = self.width, self.height = constants.width, constants.height
        self.screen = pygame.display.set_mode(self.size)
        self.clock  = pygame.time.Clock()

        # Initialize Background
        self.background = sprites.Background('stars.png')

        # Initialize Players
        self.player1 = sprites.Player(1)
        self.player2 = sprites.Player(2)

        # Initialize Scoreboard
        self.scoreboards = pygame.sprite.Group()
        self.scoreboards.add(sprites.Scoreboard(1, constants.width/4, self.player1))
        self.scoreboards.add(sprites.Scoreboard(2, 3*constants.width/4, self.player2))

        # Initialize Platforms
        self.platforms = pygame.sprite.Group()
        platform1 = sprites.Platform(constants.width/2, 50, self.player1)
        platform2 = sprites.Platform(constants.width/2, constants.height - 50, self.player2)
        self.platforms.add(platform1)
        self.platforms.add(platform2)

        # Initialize Balls
        self.balls  = pygame.sprite.Group()
        self.ball1 = sprites.Ball(platform1)
        self.ball2 = sprites.Ball(platform2)
        self.ball1.other = self.ball2
        self.ball2.other = self.ball1
        self.balls.add(self.ball1)
        self.balls.add(self.ball2)

        # Initialize Bricks
        self.bricks = pygame.sprite.Group()
        for x in range(0,16):
            for y in range(0,15):
                if y == 7:
                    brick = sprites.Brick(x * constants.brickWidth, 200 + y * constants.brickHeight, True)
                else:
                    brick = sprites.Brick(x * constants.brickWidth, 200 + y * constants.brickHeight, False)
                self.bricks.add(brick)

        # Keys Can Be Held
        pygame.key.set_repeat(500, 30)

        # Main Loop
        playing = True
        while playing:
            self.clock.tick(60)

            # Check for Win (technically checking for a loss)
            if self.player1.lives <= 0:
                print("Player 2 Wins!")
                playing = False
            elif self.player2.lives <= 0:
                print("Player 1 Wins!")
                playing = False

            # User Input Handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                for platform in self.platforms:
                    platform.update(event)
                for balls in self.balls:
                    balls.update(event)

            # Tick
            self.scoreboards.update()
            self.balls.update()
            self.bricks.update()

            # Check for Collisions and Calculate Points
            for ball in self.balls:
                for brick in pygame.sprite.spritecollide(ball, self.bricks, False, intersects):
                    ball.collided(brick, "brick")
                for platform in pygame.sprite.spritecollide(ball, self.platforms, False, intersects):
                    ball.collided(platform, "platform")

            # Draw Sprites
            self.screen.fill(constants.black)
            self.screen.blit(self.background.image, self.background.rect)
            for scoreboard in self.scoreboards:
                self.screen.blit(scoreboard.image, scoreboard.rect)
            for platform in self.platforms:
                self.screen.blit(platform.image, platform.rect)
            for brick in self.bricks:
                self.screen.blit(brick.image, brick.rect)
            for ball in self.balls:
                pygame.draw.circle(self.screen, ball.color, ball.rect.center, ball.radius)
            pygame.display.flip()
            
        pygame.quit()

if __name__ == '__main__':
    gs = BrickBreaker()
    gs.run()
