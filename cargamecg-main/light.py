# copy 
import pygame, random
from pygame.locals import *

 
class light:
    def __init__(self, shad, file):
        shad.lights.append(self)

        self.images = []
        #self.surface = fog   # surface to render light on        

###    def add(self, file):
        self.images.append( pygame.image.load(file) )
        self.img_number = 0
        self.img = self.images[ self.img_number ]
        
        self.rect = self.img.get_rect()
        self.pos = ()
        self.angle = 0
        
        shad.lights.append( light )    
        print(shad.lights)

# others

        self.counter = 0
        self.switch = None


    def add_img(self, img):   # img = pygame.image.load(path)
        self.images.append(img)


    def setup(self, pos, angl=0, switch=(0, 0)): # switch = (min, max)
        self.pos = list(pos)
        self.angle = angl

        if switch != None:
            self.switch = switch
            self.counter = random.randint(self.switch[0], self.switch[1])


    def next_img(self):  # swithing to next light image
        self.counter = random.randint(self.switch[0], self.switch[1])
        self.img_number += 1
        
        if self.img_number >= len(self.images):
            self.img_number -= len(self.images)

        self.img = self.images[ self.img_number ]
        self.rect = self.img.get_rect()
   
    
    def render(self, fog, pos):
        new_img = pygame.transform.rotate(self.img, self.angle)
        new_rect = new_img.get_rect()
        new_rect.center = self.rect.center

        self.rect = new_rect
        #fog.blit(self.img, self.rect)
        fog.blit(new_img, self.rect)
        
        #fog.blit(self.img, self.rect)











### render darknes (fog)
##    fog.fill(fog_color)
##
##    light_rect.center = player_rect.center
##
##    if switch == 1:
##        fog.blit(light_mask, light_rect)
##
##    window.blit(fog, (0, 0), special_flags=BLEND_MULT)  # color from 0 to 1; multiplied
