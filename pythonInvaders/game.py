#!/usr/bin/python

try:
    import sys
    import pygame
    from random import randint
    #from pygame.locals import *
except ImportError, err:
    print "Failed to load module. %s" % (err)

windowTitle = 'Python Invaders'

enemieSprite = 'data/enemie.png'
projectileSprite = 'data/projectile.png'
playerSprite = 'data/player.png'

screenWidth = 800
screenHeight = 600
  
class Entity: 
  
    def __init__(self, xPos, yPos, width, height, speed):
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.movementSpeed = speed

    def inside(self, x, y, width, height):
        a = self.xPos > x and (self.xPos + self.width) < x + width
        b = self.yPos > y and (self.yPos + self.height) < y + height
        return a and b

    def intersects(self, x, y, width, height):
        a = (self.xPos >= x and self.xPos < (x + width) or (
            (self.xPos + self.width) > x and (self.xPos + self.width) <= (x + width)))
        b = (self.yPos >= y and self.yPos < (y + height) or (
            (self.yPos + self.height) > y and (self.yPos + self.height) <= (y + height)))
        return a and b 

class Blinker:
  
    blinkInterval = 10
    blinks = 3

    def __init__(self):
        self.accumulatedTime = 0
        self.accumulatedBlinks = 0
        self.active = False
        self.shouldD = False

    def activate(self):
        self.active = True

    def shouldDraw(self):
        return not self.active or self.shouldD

    def update(self, time):
        if not self.active:
            return
    
        self.accumulatedTime += time    
        if self.accumulatedTime > Blinker.blinkInterval:
            self.accumulatedTime = 0
            self.shouldD = not self.shouldD
            self.accumulatedBlinks += 1
    
        if self.accumulatedBlinks >= Blinker.blinks:
            self.active = False
            self.accumulatedBlinks = 0
            self.shouldD = False

class Player(Entity):
  
    shootCoolDown = 200.0 # Five shoots each second
    
    def __init__(self, screen, projectiles, enemieProjectiles):
        self.screen = screen
        self.projectiles = projectiles
        self.enemieProjectils = enemieProjectiles
        self.playerSprite = pygame.image.load(playerSprite).convert_alpha()
        Entity.__init__(self, screenWidth / 2, screenHeight - 50, 
                        self.playerSprite.get_width(), 
          self.playerSprite.get_height(), 5.0)
        self.halfWidth = self.width / 2.0
        self.shootCoolDownCounter = 0
        self.hp = 5
        self.blinker = Blinker()

    def update(self, keys, time):
        self.shootCoolDownCounter += time
        canShoot = self.shootCoolDownCounter >= self.shootCoolDown
        
        if canShoot and keys[pygame.K_SPACE]:
            self.shootCoolDownCounter = 0.0
            # TODO This assumes that the Player and The Projectil has the same
            # width.
            projectile = Projectile(self.screen, self.xPos, self.yPos, -1)
            self.projectiles.append(projectile)
        
        direction = 0
        if keys[pygame.K_RIGHT]: 
            direction = 1
        if keys[pygame.K_LEFT]: 
            direction = -1
        
        if direction != 0:
            self.xPos += direction * self.movementSpeed
        
        if not self.inside(0, 0, screenWidth, screenHeight):
            self.xPos += -direction * self.movementSpeed
            
        hurt = False
        for e in self.enemieProjectils:
            hurt = e.intersects(self.xPos, self.yPos, self.width, self.height)
            if hurt:
                self.enemieProjectils.remove(e)
                break
        if hurt:
            self.hp = self.hp - 1
            self.blinker.activate()
        
        self.blinker.update(1)
        
        if self.blinker.shouldDraw():
            self.screen.blit(self.playerSprite, (self.xPos, self.yPos))
            
    def isAlive(self):
        return self.hp >= 0
    
class Projectile(Entity):

    def __init__(self, screen, x, y, direction):
        self.sprite = pygame.image.load(projectileSprite).convert_alpha()
        Entity.__init__(self, x, y, self.sprite.get_width(), 
          self.sprite.get_height(),  10.0)
        self.screen = screen
        self.direction = direction

    def update(self):
        self.yPos += self.movementSpeed * self.direction
        self.screen.blit(self.sprite, (self.xPos, self.yPos))

class Enemie(Entity):

    chanceOfShooting = 1000
    speed = 0
    
    def __init__(self, screen, x, y, enemieShoots):
        self.oldXPos = x
        self.screen = screen
        self.direction = 1
        self.sprite = pygame.image.load(enemieSprite).convert_alpha()
        Entity.__init__(self, x, y + 10, self.sprite.get_width(), 
          self.sprite.get_height(), Enemie.speed)
        self.hp = 3
        self.blinker = Blinker()
        self.enemieShoots = enemieShoots

    def update(self):
        self.oldXPos = self.xPos
        self.xPos += self.direction * self.movementSpeed
        self.blinker.update(1)
        if self.blinker.shouldDraw():
            self.screen.blit(self.sprite, (self.xPos, self.yPos))
        
        if randint(0, Enemie.chanceOfShooting) == Enemie.chanceOfShooting:
            projectile = Projectile(self.screen, self.xPos, self.yPos, 1)
            self.enemieShoots.append(projectile)
    
    def switchDirection(self):
        self.direction = -self.direction
    
    def moveDown(self):
        self.yPos += self.height
    
    def resetToOldPosition(self):
        self.xPos = self.oldXPos
    
    def hurt(self):
        self.blinker.activate()
        self.hp = self.hp - 1
    
    def isAlive(self):
        return self.hp > 0
    
class EnemieManager:

    rows = 10
    columns = 3
    
    xSpacing = 40
    ySpacing = 30
    
    def __init__(self, screen, playerShoots, enemieShots):
        self.screen = screen
        self.playerShoots = playerShoots
        self.enemieShoots = enemieShots
        self.enemies = []
        self.createEnemies()
    
    def createEnemies(self):
        Enemie.speed = Enemie.speed + 1
        if Enemie.chanceOfShooting > 100:
            Enemie.chanceOfShooting = Enemie.chanceOfShooting - 200 
        for i in range(0, EnemieManager.columns):
            for j in range(0, EnemieManager.rows):
                self.enemies.append(Enemie(self.screen, 
                                           j * EnemieManager.xSpacing, 
                                           i * EnemieManager.ySpacing, 
                                           self.enemieShoots))

    def update(self):
        map(Enemie.update, self.enemies)
        for x in self.enemies:
            for p in self.playerShoots:
                if p.intersects(x.xPos, x.yPos, x.width, x.height):
                    self.playerShoots.remove(p)
                    x.hurt()
                    if not x.isAlive():
                        self.enemies.remove(x)
        
            # TODO Remove the hardecoded screen stuff :o
            if not x.inside(0, 0, screenWidth, screenHeight):
                map(Enemie.switchDirection, self.enemies)
                map(Enemie.moveDown, self.enemies)
                map(Enemie.resetToOldPosition, self.enemies)
        
            if len(self.enemies) == 0:
                self.createEnemies()
                
    def intersectWithEnemies(self, x, y, width, height):
        
        for e in self.enemies:
            if e.intersects(x, y, width, height):
                return True
            
        return False

def main():

    pygame.init()
    
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption(windowTitle)
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    
    pygame.display.flip()
    
    playerProjectiles = []
    enemieProjectiles = []
    player = Player(screen, playerProjectiles, enemieProjectiles)
    enemiManager = EnemieManager(screen, playerProjectiles, enemieProjectiles)
    
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
        
        playerProjectiles[:] = [proj for proj in playerProjectiles 
                          if proj.intersects(0, 0, screenWidth, screenHeight)]
        
        enemieProjectiles[:] = [proj for proj in enemieProjectiles 
                          if proj.intersects(0, 0, screenWidth, screenHeight)]
        
        map(Projectile.update, playerProjectiles)
        map(Projectile.update, enemieProjectiles)
        
        pygame.display.flip()
        
        if enemiManager.intersectWithEnemies(player.xPos, player.yPos, 
                                             player.width, player.height):
            #TODO Fix some game over text when the player dies.
            break
        
        if not player.isAlive():
            break
                
if __name__ == '__main__': main()

