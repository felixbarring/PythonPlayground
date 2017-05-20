try:
	import sys
	import os
	import pygame
	from pygame.locals import *
except ImportError, err:
  print "Failed to load module. %s" % (err)
  

def main():
  pygame.init()
  screen = pygame.display.set_mode((640, 480))
  pygame.display.set_caption('Python Invaders')

  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((0, 0, 0))

  screen.blit(background, (0,0))
  pygame.display.flip()

  while True:
    for event in pygame.event.get():
      if (event.type == pygame.QUIT or event.type == pygame.KEYDOWN 
          and event.key == pygame.K_ESCAPE) : 
        sys.exit()

    pygame.display.flip()
                
if __name__ == '__main__': main()
