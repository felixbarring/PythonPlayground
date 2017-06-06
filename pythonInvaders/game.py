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

  def inside(self, x, y, width, height):
    return ((self.xPos > x and (self.xPos + self.width) < x + width) and (
            self.yPos > y and (self.yPos + self.height) < y + height))

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
      projectile = Projectile(self.screen, self.xPos + self.halfWidth, 
        self.yPos, -1)
      self.projectiles.append(projectile)
    
    direction = 0
    if keys[pygame.K_RIGHT]: 
      direction = 1
    if keys[pygame.K_LEFT]: 
      direction = -1

    if direction != 0:
      self.xPos += direction * self.movementSpeed

    # TODO Remove the hardcode of the screen size...
    if not self.inside(0, 0, 800, 600):
      self.xPos += -direction * self.movementSpeed

    self.screen.blit(self.playerSprite, (self.xPos, self.yPos))
    
class Projectile(Entity):
  screen = None
  sprite = None

  direction = None

  def __init__(self, screen, x, y, direction):
    self.sprite = pygame.image.load('data/projectile.png').convert()
    Entity.__init__(self, x, y, self.sprite.get_width(), 
      self.sprite.get_height(),  10.0)
    self.screen = screen
    self.direction = direction

  def update(self):
    self.yPos += self.movementSpeed * self.direction
    self.screen.blit(self.sprite, (self.xPos, self.yPos))

class Enemie(Entity):
  screen = None
  direction = None
  sprite = None

  def __init__(self, screen, x, y):
    self.screen = screen
    self.direction = 1
    self.sprite = pygame.image.load('data/player.png').convert()
    Entity.__init__(self, x, y + 10, self.sprite.get_width(), 
      self.sprite.get_height(), 0)

  def update(self):
    self.xPos += self.direction
    self.screen.blit(self.sprite, (self.xPos, self.yPos))

  def switchDirection(self):
    self.direction = -self.direction

  def moveDown(self):
    self.yPos += self.height
    

class EnemieManager:
  screen = None
  enemies = None

  rows = 10
  columns = 3

  def __init__(self, screen):
    self.screen = screen
    self.enemies = []
    
    for i in range(0, self.columns):
      for j in range(0, self.rows):
        self.enemies.append(Enemie(self.screen, j * 40, i * 30))

  def update(self):
    map(Enemie.update, self.enemies)
    switch = False
    for x in self.enemies:
      if not x.inside(0, 0, 800, 600):
        switch = True
        break
    if switch:
      map(Enemie.switchDirection, self.enemies)
      map(Enemie.moveDown, self.enemies)


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
  enemiManager = EnemieManager(screen)

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
    enemiManager.update()

    projectiles[:] = [proj for proj in projectiles 
      if proj.intersects(0, 0, screenWidth, screenHeight)]

    for projectile in projectiles:
      projectile.update()

    pygame.display.flip()
                
if __name__ == '__main__': main()

