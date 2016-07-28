# Import a library of functions called 'pygame'
import pygame
import pygame._view
import random
import math
from Player import *
from Button import *


# Initialize the dream engine
pygame.init()

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
NICEBLUE = ( 141, 236, 232)
ORANGE   = ( 255, 172,  79)
YELLOW   = ( 255, 255,   0)

size = (700,500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Slay the Sexymon")

#GAME CONSTANTS

Score_max = 5
Win = False
Lose = False
boss_level = False
Time = 1
start_time = 50
row = 0

#Knight
Knight = Player("..//Slay the Dragon//Graphics//Knight.gif",10,(350,200),(100,100))

#Boss Dragon

Dragon = Fire("..//Slay the Dragon//Graphics//Dragon.gif",20,)

# Castle Constants
Castle = pygame.image.load("..//Slay the Dragon//Graphics//Castle.gif")
Castle.set_colorkey(BLACK)
Castle_size = (200,150)

#Enemies
Sexymon = pygame.image.load("..//Slay the Dragon//Graphics//Enemy.gif")
Sexymon.set_colorkey(BLACK)
Sexymon_Hit = pygame.mixer.Sound("..//Slay the Dragon//Sound//Hit.wav")
Sexy = pygame.mixer.Channel(1)
Sexy_rect = pygame.Rect(Sexymon.get_rect())
Sexymon.set_colorkey(BLACK)
Enemies = []

    #Powered up
Sexymon_power = pygame.image.load("..//Slay the Dragon//Graphics//Enemy_power.gif")
Sexymon_power.set_colorkey(BLACK)
speed_bonus = 5

#Blaster
Hadouken = pygame.image.load("..//Slay the Dragon//Graphics//hadouken.gif")
Hadouken.set_colorkey(BLACK)
Hadouken_sound = pygame.mixer.Sound("..//Slay the Dragon//Sound//Shotgun.wav")
Hdkn = pygame.mixer.Channel(2)
Hdkn.set_volume(0.1)
Hadouken.set_colorkey(BLACK)
Shot_max = 0
Shots_time = Shot_max
Shots = []
Fire = False

#Loop until the user clicks the close button.

done = False
again = True

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while again:

    while not done:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True  # Flag that we are done so we exit this loop
                again = False
            elif pygame.mouse.get_pressed()[0] and Shots_time >= Shot_max:
                Shots_time = 0

                Shots.append([Knight.x2 ,Knight.y2 ,Knight.facing,True])
                Hdkn.play(Hadouken_sound)

        if Time % 32 == 0 and not boss_level and Time >= start_time + 10:
            direction = random.choice((-1,1))
            Bady = random.randrange(0,size[1] - 50)
            bad_power = random.randrange(8,12)
            if direction == 1:
                Enemies.append([0,Bady,direction,True,bad_power])
            else:
                Enemies.append([size[0],Bady,direction,True,bad_power])

        if Time % 50 == 0 and boss_level:
            c1 = Dragon.calculate_trajectory(Knight)
            Dragon.Channel.play(Dragon.Fire,0)
            if Dragon.facing == -1:
                Dragon.Shots.append([Dragon.mouthx , Dragon.mouthy, c1[1],True])
            if Dragon.facing == 1:
                Dragon.Shots.append([Dragon.mouthx - 121, Dragon.mouthy, c1[1],True])
        elif Time % 30 == 0 and not boss_level:
            c1 = Dragon.calculate_trajectory(Knight)
            Dragon.Shots.append([Dragon.mouthx -121, Dragon.mouthy, c1[1],True])

        if Knight.Score >= Score_max and Dragon.ready:
            Dragon.Channel.play(Dragon.Enter,0)
            boss_level = True
            Dragon.ready = False


        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
        pos = pygame.mouse.get_pos()
        if Time >= start_time:

            Knight.x2 = pos[0]
            Knight.y2 = pos[1]

        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        if not boss_level:
            screen.fill(BLUE)
        else:
            screen.fill(RED)

        #Castle
        screen.blit(Castle,(250,0))

        Knight.draw_bars(screen)

        #Knight
        if Knight.x2 < Knight.x1:
            screen.blit(Knight.Image,(Knight.x2 - 50,Knight.y2 - 50))
            Knight.facing = -1
        elif Knight.x2 > Knight.x1:
            screen.blit(pygame.transform.flip(Knight.Image,True,False),(Knight.x2 - 50,Knight.y2 - 50))
            Knight.facing = 1
        elif Knight.x2 == Knight.x1:
            if Knight.facing == 1:
                screen.blit(pygame.transform.flip(Knight.Image,True,False),(Knight.x2 - 50,Knight.y2 - 50))
            elif Knight.facing == -1:
                screen.blit(Knight.Image,(Knight.x2 - 50, Knight.y2 - 50))

        Knight_rect = pygame.Rect(Knight.Image.get_rect())
        Knight_rect.left = Knight.x2
        Knight_rect.top = Knight.y2

        Dragon_rect = pygame.Rect(Dragon.Image.get_rect())
        Dragon_rect.left = Dragon.x2 - 60
        Dragon_rect.top = Dragon.y2 - 60

        if boss_level:
            #Dragon follow
            coordinates = Dragon.calculate_trajectory(Knight)
            if abs(coordinates[4]) <= 95 and abs(coordinates[5]) <= 80:
                pass
            else:
                Dragon.x2 += coordinates[2]
                Dragon.y2 += coordinates[3]

            #Dragon movement
            if Dragon.x2 < Dragon.x1:
                screen.blit(Dragon.Image,(Dragon.x2 - 95,Dragon.y2 - 95))
                Dragon.facing = 1
            elif Dragon.x2 > Dragon.x1:
                screen.blit(pygame.transform.flip(Dragon.Image,True,False),(Dragon.x2 - 95,Dragon.y2 - 95))
                Dragon.facing = -1
            elif Dragon.x2 == Dragon.x1:
                if Dragon.facing == 1:
                    screen.blit(pygame.transform.flip(Dragon.Image,True,False),(Dragon.x2 - 95,Dragon.y2 - 95))
                elif Dragon.facing == -1:
                    screen.blit(Dragon.Image,(Dragon.x2 - 95, Dragon.y2 - 95))

            # Dragon damage

            if Dragon_rect.colliderect(Knight_rect):
                Knight.Health -= 1
                Dragon.Channel.play(Dragon.Touch,0)
                Dragon.x2 += 100 * Dragon.facing
                Dragon.y2 += random.randrange(-100,100)

            #Dragon shot
            if Dragon.facing == 1:

                Dragon.mouthx = Dragon.mouth[0] + Dragon.x2 - 95
                Dragon.mouthy = Dragon.mouth[1] + Dragon.y2 - 75
            else:
                Dragon.mouthx = Dragon.mouth_flip[0] + Dragon.x2 - 95
                Dragon.mouthy = Dragon.mouth_flip[1] + Dragon.y2 - 75

            ki_index = 0
            for ki in Dragon.Shots:

                ki[0] += int(10 * math.cos(ki[2]))
                ki[1] += int(10 * math.sin(ki[2]))


                index_fireball = 0

                kirect = pygame.Rect(Dragon.Fireball_0.get_rect())
                kirect.left = ki[0]
                kirect.top = ki[1]

                if kirect.colliderect(Knight_rect):
                   ki[3] = False
                   Knight.Health -= 2
                   Sexymon_Hit.play()
                if ki[0]>size[0] or ki[0]< - 100:
                    ki[3] = False
                elif ki[1] > size[1] or ki[1] < -50:
                    ki[3] = False

                ki_index += 1

            #Draw all fireballs
            blast_index = 0
            for blasts in Dragon.Shots:

                if blasts[3]:
                    new_fire = pygame.transform.rotate(Dragon.Fireball_0, ((-180 / math.pi) *blasts[2]))
                    screen.blit(new_fire, (blasts[0],blasts[1] - 20))
                else:
                    Dragon.Shots.pop(blast_index)

                blast_index += 1

        #Enemy Movement

        for dudes in Enemies:
            bad_index = 0
            bad_velx = 10 * dudes[2]
            dudes[0] += bad_velx

        #Fast enemy power up
            if dudes[4] == 10:
                dudes[0] += speed_bonus * dudes[2]

            if dudes[0]>size[0] or dudes[0]< - 50:
                dudes[3] = False
            sexy_rect = pygame.Rect(Sexymon.get_rect())
            sexy_rect.left = dudes[0]
            sexy_rect.top = dudes[1]

        #Collison
            index_fireball = 0
            for fireball in Shots:
                Firect=pygame.Rect(Hadouken.get_rect())
                Firect.left=fireball[0]
                Firect.top=fireball[1]
                if sexy_rect.colliderect(Firect):
                    if dudes[3]:
                        Knight.Score += 1
                    dudes[3] = False
                    fireball[3] = False

                index_fireball += 1
            if sexy_rect.colliderect(Knight_rect):
                if dudes[4] == 10:
                    Knight.Health -= 3
                else:
                    Knight.Health -= 1
                Sexy.play(Sexymon_Hit)
                dudes[3] = False

            bad_index+=1
        sexy_index = 0

        # Draw all Sexymons
        for machos in Enemies:

            if machos[3] and machos[4] == 10:
                screen.blit(Sexymon_power,(machos[0],machos[1]))
            elif machos[3]:
                screen.blit(Sexymon, (machos[0],machos[1]))
            else:
                Enemies.pop(sexy_index)

            sexy_index +=1

        #Shooting

        for bullet in Shots:

            velx = 12 * bullet[2]
            bullet[0] += velx

            if bullet[0]<-64 or bullet[0]>size[0] or bullet[1]<-64 or bullet[1]>size[1]:
                bullet[3] = False
            if boss_level:

                Firect = pygame.Rect(Hadouken.get_rect())
                Firect.left = bullet[0]
                Firect.top = bullet[1]
                if Dragon_rect.colliderect(Firect):
                   Dragon.Health-=1
                   bullet[3] = False

        index_shoot = 0
        for projectile in Shots:
            if projectile[3]:
                screen.blit(Hadouken, (projectile[0], projectile[1]))
            else:
                Shots.pop(index_shoot)

            index_shoot+=1

        pygame.display.flip()

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        #Post Drawing game logic below

        Knight.x1 = Knight.x2
        Knight.y1 = Knight.y2
        Dragon.x1 = Dragon.x2
        Dragon.y1 = Dragon.y2

        #Post Drawing game logic above

        if Knight.Health <= 0:
            done = True
            Lose = True
        if Knight.Score >= Score_max and Dragon.Health == 0:
            done = True
            Win = True
        Shots_time +=1
        Time +=1

        #Fps

        clock.tick(32)

    if Win:
        screen.fill(GREEN)
        font = pygame.font.Font(None, 100)
        text = font.render("EXCELLENT!", True, ORANGE)
        screen.blit(text, [150,200])
        pygame.display.flip()
        pygame.time.wait(1000)
        screen.fill(GREEN)
        line1 = font.render("THE SEXYMON AND", True, ORANGE)
        line2 = font.render("THE DRAGON", True, ORANGE)
        line3 = font.render("ARE DEAD!", True, ORANGE)
        screen.blit(line1,[10,100])
        screen.blit(line2, [120,200])
        screen.blit(line3, [160,300])
        pygame.display.flip()
        pygame.time.wait(5000)
        Win = False

    if Lose:
        screen.fill(RED)
        font = pygame.font.Font(None, 100)
        text = font.render("YOU SUCK!", True, YELLOW)
        screen.blit(text, [150,200])
        pygame.display.flip()
        pygame.time.wait(1000)
        Lose = False

    if again:
        screen.fill(BLUE)
        font = pygame.font.Font(None, 100)
        text = font.render("AGAIN?",True,YELLOW)
        screen.blit(text,[210,50])

        Yes = Button(ORANGE,"YES",GREEN,[50,200,200,100])
        No = Button(ORANGE,"NO", RED, [450,200,200,100])

        Yes.draw(screen)
        No.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If user clicked close
                again = False

        elif pygame.mouse.get_pressed()[0]:

            if Yes.get_click():
                done = False
                Knight.back_to_life()
                Dragon.back_to_life()
                boss_level = False

            elif No.get_click():

                again = False

    pygame.display.flip()

pygame.quit()