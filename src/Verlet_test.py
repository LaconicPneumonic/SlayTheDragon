import pygame
from Gravity import *

pygame.init()

size = (700,700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Physics test")

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
NICEBLUE = ( 141, 236, 232)
ORANGE   = ( 255, 172,  79)
YELLOW   = ( 255, 255,   0)

clock = pygame.time.Clock()

done = False


Bob = GravityGuy()
Bob.screen_center = (350,350)

Bob.time_step = .1

Bob.y = 100
Bob.v_y = 0

Bob.x = 350
Bob.v_x = 70


Sexymon = pygame.image.load("../Slay the Dragon/Graphics/Enemy.gif")


while not done:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif pygame.mouse.get_pressed()[0]:
            Bob.hop = True

    screen.fill(BLUE)

    screen.blit(Sexymon,Bob.orbit())

    pygame.display.flip()

    #clock.tick(100)

pygame.quit()