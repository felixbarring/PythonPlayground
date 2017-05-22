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
  projectiles = None
  
  xPos = 400.0
  yPos = 550.0

  movementSpeed = 0.1

  def __init__(self, screen, projectiles):
    self.screen = screen
    self.projectiles = projectiles
    self.playerSprite = pygame.image.load('data/player.png').convert()

  def update(self, keys):
    if keys[pygame.K_RIGHT]: 
      self.xPos += self.movementSpeed

    if keys[pygame.K_LEFT]: 
      self.xPos -= self.movementSpeed
    
    if keys[pygame.K_SPACE]:
#      projectile = Projectile(self.screen, self.xPos, self.yPos, -1)
      self.projectiles.append(projectile)

    self.screen.blit(self.playerSprite, (self.xPos, self.yPos))
    
class Projectile:
  screen = None
  sprite = None

  xPos = None
  yPos = None

  movementSpeed = 0.3
  direction = None

  def __init__(self, screen, x, y, direction):
    self.screen = screen
    self.sprite = pygame.image.load('data/projectile.png').convert()
    self.xPos = x
    self.yPos = y
    self.direction = direction

  def update(self):
    self.yPos += self.movementSpeed * self.direction
    self.screen.blit(self.sprite, (self.xPos, self.yPos))

def main():

  pygame.init()
  screen = pygame.display.set_mode((screenWidth, screenHeight))
  pygame.display.set_caption('Python Invaders')

  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((0, 0, 0))

  screen.blit(background, (0,0))
  pygame.display.flip()

  projectiles = []
  player = Player(screen, projectiles)

  while True:
    for event in pygame.event.get():
      if (event.type == pygame.QUIT or event.type == pygame.KEYDOWN 
          and event.key == pygame.K_ESCAPE) : 
        sys.exit()

    keys = pygame.key.get_pressed()

    player.update(keys)

    for projectile in projectiles:
      projectile.update()

    pygame.display.flip()
                
if __name__ == '__main__': main()

