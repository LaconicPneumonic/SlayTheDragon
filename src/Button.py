import pygame
import math

# Initialize the dream engine
pygame.init()

class Button(pygame.Rect):

    bevel_color = (255,255,255)

    def __init__(self, color, text, text_color, size):
        self.color = color

        self.text = text

        self.text_color = text_color

        pygame.Rect.__init__(self,size)



    def get_click(self):
        pos = pygame.mouse.get_pos()

        if self.collidepoint(pos):
            return True
        else:
            return False


    def text_size(self):
        x = (self.width - 10) / (len(self.text)/2)
        return x




    def draw(self,Surface):
        corner = [self.left,self.top]
        definition = [self.width,self.height]
        bevel = 3

        pygame.draw.rect(Surface,self.bevel_color,corner+definition,0)

        shape = map(lambda stuff: stuff + bevel, corner)
        shape += map(lambda stuff: stuff - (2 * bevel), definition)



        pygame.draw.rect(Surface,self.color,shape,0)

        font = pygame.font.Font(None, self.text_size())

        text = font.render(self.text, True, self.text_color)

        mid_X = self.width / 2 - font.size(self.text)[0] / 2 + self.left
        mid_Y = self.height / 2 - font.size(self.text)[1] / 2 + self.top


        Surface.blit(text, (mid_X,mid_Y))
