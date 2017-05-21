#!/usr/bin/python

try:
	import sys
	import os
	import pygame
	from pygame.locals import *
except ImportError, err:
  print "Failed to load module. %s" % (err)
  
screenWidth = 800
screenHeight = 600

class Player:
  screen = None
  playerSprite = None
  
  xPos = 400.0
  yPos = 550.0

  movementSpeed = 0.1

  def __init__(self, s):
    print "### Player \n"
    self.screen = s
    self.playerSprite = pygame.image.load('data/player.png').convert()

  def update(self, moveLeft, moveRight):
    if moveLeft: self.xPos += self.movementSpeed
    if moveRight: self.xPos -= self.movementSpeed
    self.screen.blit(self.playerSprite, (self.xPos, self.yPos))

def main():

  print "### Main \n"

  pygame.init()
  screen = pygame.display.set_mode((screenWidth, screenHeight))
  pygame.display.set_caption('Python Invaders')

  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((0, 0, 0))

  screen.blit(background, (0,0))
  pygame.display.flip()

  player = Player(screen)

  while True:
    for event in pygame.event.get():
      if (event.type == pygame.QUIT or event.type == pygame.KEYDOWN 
          and event.key == pygame.K_ESCAPE) : 
        sys.exit()
      
      moveRight = event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT
      moveLeft = event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT

    player.update(moveRight, moveLeft)
    pygame.display.flip()
                
if __name__ == '__main__': main()
