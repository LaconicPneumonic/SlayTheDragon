import pygame
import pygame._view
import math
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
NICEBLUE = ( 141, 236, 232)
ORANGE   = ( 255, 172,  79)
YELLOW   = ( 255, 255,   0)

pygame.init()
size = (700, 500)
screen = pygame.display.set_mode(size)
class Player():
    def __init__(self,Image,Health,start_pos,size):
        self.Image = pygame.image.load(Image)
        self.Image.set_colorkey(BLACK)

        self.Health = Health
        self.Health_max = Health

        self.start_pos = start_pos
        self.size = size



        self.x1,self.y1,self.x2,self.y2 = start_pos[0],start_pos[1],start_pos[0],start_pos[1]

    ScoreCat = pygame.image.load("..//Slay the Dragon//Graphics//Score CAt.gif")
    ScoreCat.set_colorkey(BLACK)

    # Health Bar

    def draw_bars(self,Surface):
        pygame.draw.rect(Surface,NICEBLUE,[20,20,104,10],0)
        pygame.draw.rect(Surface,GREEN,[20,20,104,10],2)
        block_width = int(100/self.Health_max)
        for i in xrange(self.Health_max - self.Health):
            pygame.draw.rect(screen,RED,[22 + block_width * i,22,10,6],0)

        if self.Score > 0:
            if self.Score % 5 == 0 and self.Score != self.Score2 and self.row < 20:
                    self.row += 1


            for i in xrange(self.Score):
                Surface.blit(self.ScoreCat, (475 + 40 *(i % 5),20 + (50 * self.row)))

    def back_to_life(self):
        self.Health = self.Health_max


    facing = -1
    row = 0
    Score = 0
    Score2 = 0


class Boss():
    def __init__(self,Image,Health):
        self.Image = pygame.image.load(Image)
        self.Image.set_colorkey(WHITE)
        self.Health = Health
        self.Health_orig = Health
        self.x1,self.x2,self.y1,self.y2 = 0,0,0,0


    def calculate_trajectory(self,Player):
        delta_x = Player.x2 - self.x2
        delta_y = Player.y2 - self.y2

        angle = math.atan2(delta_y , delta_x)

        r = int(((delta_x ** 2) + (delta_y ** 2)) ** .5)


        return r , angle, math.copysign(self.speed,delta_x), math.copysign(self.speed,delta_y),delta_x,delta_y



class Fire(Boss):


    Fireball_0 = pygame.image.load("..//Slay the Dragon//Graphics//Fireball-0.gif")


    Fireball_0.set_colorkey(BLACK)

    Channel = pygame.mixer.Channel(4)

    Enter = pygame.mixer.Sound("..//Slay the Dragon//Sound//Dragon enter.wav")

    Touch = pygame.mixer.Sound("..//Slay the Dragon//Sound//Dragon touch.wav")
    Fire = pygame.mixer.Sound("..//Slay the Dragon//Sound//Dragon fire.wav")

    mouthx = 121
    mouthy = 41
    facing = -1
    speed = 2
    Shots = []

    def back_to_life(self):
        self.Health = self.Health_orig
        self.x1,self.y1 = 0,0
        self.Shots = []

    mouth = [121, 41]
    mouth_flip = [29,41]
