#!/usr/bin/python

try:
  import sys
  import os
  import pygame
  from pygame.locals import *
except ImportError, err:
  print "Failed to load module. %s" % (err)
  
class Entity: 
  xPos = None
  yPos = None

  width = None
  height = None
    
  movementSpeed = None
  
  def __init__(self, xPos, yPos, width, height, speed):
    self.xPos = xPos
    self.yPos = yPos
    self.width = width
    self.height = height
    self.movementSpeed = speed

  # Overlapping?
  def intersects(self, x, y, width, height):
    return ((self.xPos > x and self.xPos < (x + width) or 
            ((self.xPos + self.width) > x and (self.xPos + self.width) < (x + width))) and (
            (self.yPos > y and self.yPos < (y + height) or  
            ((self.yPos + self.height) > y and (self.yPos + self.height) > (y + height)))))

class Player(Entity):
  screen = None
  playerSprite = None
  projectiles = None
  
  shootCoolDownCounter = 0.0
  shootCoolDown = 200.0 # Five shoots each second :-)

  halfWidth = None

  def __init__(self, screen, projectiles):
    self.screen = screen
    self.projectiles = projectiles
    self.playerSprite = pygame.image.load('data/player.png').convert()
    Entity.__init__(self, 400, 550, self.playerSprite.get_width(), 
      self.playerSprite.get_height(), 5.0)
    self.halfWidth = self.width / 2.0

  def update(self, keys, time):
    self.shootCoolDownCounter += time
    canShoot = self.shootCoolDownCounter >= self.shootCoolDown

    if canShoot and keys[pygame.K_SPACE]:
      self.shootCoolDownCounter = 0.0
      print self.width
      projectile = Projectile(self.screen, self.xPos + self.halfWidth, 
        self.yPos, -1)
      self.projectiles.append(projectile)

    if keys[pygame.K_RIGHT]: 
      self.xPos += self.movementSpeed

    if keys[pygame.K_LEFT]: 
      self.xPos -= self.movementSpeed

    self.screen.blit(self.playerSprite, (self.xPos, self.yPos))
    
class Projectile(Entity):
  screen = None
  sprite = None

  direction = None

  def __init__(self, screen, x, y, direction):
    self.sprite = pygame.image.load('data/projectile.png').convert()
    Entity.__init__(self, x, y, self.sprite.get_width(), 
      self.sprite.get_height(),  3.0)
    self.screen = screen
    self.direction = direction

  def update(self):
    self.yPos += self.movementSpeed * self.direction
    self.screen.blit(self.sprite, (self.xPos, self.yPos))

def main():

  pygame.init()

  screenWidth = 800
  screenHeight = 600
  screen = pygame.display.set_mode((screenWidth, screenHeight))
  pygame.display.set_caption('Python Invaders')

  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((0, 0, 0))

  pygame.display.flip()

  projectiles = []
  player = Player(screen, projectiles)

  maxFps = 60
  clock = pygame.time.Clock()

  while True:
    
    timePassed = clock.tick_busy_loop(maxFps)
    screen.blit(background, (0,0))

    for event in pygame.event.get():
      if (event.type == pygame.QUIT or event.type == pygame.KEYDOWN 
          and event.key == pygame.K_ESCAPE) : 
        sys.exit()

    keys = pygame.key.get_pressed()

    player.update(keys, timePassed)

    projectiles[:] = [proj for proj in projectiles 
      if proj.intersects(0, 0, screenWidth, screenHeight)]

    for projectile in projectiles:
      projectile.update()

    pygame.display.flip()
                
if __name__ == '__main__': main()

